import random
import math

class Person:
    def __init__(self, is_employed, is_retired, is_minor):
        self.is_employed = is_employed
        self.is_retired = is_retired
        self.is_minor = is_minor
        self.wallet = random.randint(-5000, 15000)  # Salário inicial
        self.salary = random.randint(1500, 6000) if is_employed else random.randint(1000, 4000) # se for aposentado recebe menos
        self.consumption = 0

    def receive_income(self):
        amount = self.salary * (random.randint(6, 11) / 10)
        self.spend(amount)
        

    def spend(self, amount):
        self.consumption = amount # soma os gastos
        self.wallet -= amount  # Subtrair gasto do salário inicial


class Company:
    def __init__(self, sector, employees, initial_capital):
        self.sector = sector
        self.employees = employees
        self.monthly_profit = random.randint(50000, 200000)
        self.capital = initial_capital
        
        # Definindo a taxa de impostos com base no setor
        if sector == 'Industry':
            self.taxes = 0.25  # Maior taxa para indústria
        elif sector == 'Services':
            self.taxes = 0.2   # Taxa média para serviços
        elif sector == 'Commerce':
            self.taxes = 0.15  # Menor taxa para comércio

    def pay_salaries(self):
        total_salaries = 0
        for employee in self.employees:
            employee.receive_income()
            total_salaries += employee.salary

        self.capital -= total_salaries  # Subtrair pagamento de salários do capital
        return total_salaries

    def collect_taxes(self):
        tax = self.monthly_profit * self.taxes
        self.capital -= tax
        return tax

    def receive_revenue(self, amount):
        val = random.randint(math.floor(amount / 3), math.floor(amount * 2))
        self.monthly_profit += val
        self.capital += val  # Adicionar lucro ao capital


def initialize_population(total_population, unemployed, retired, minors):
    population = []
    employed = total_population - (unemployed + retired + minors)
    for _ in range(employed):
        population.append(Person(is_employed=True, is_retired=False, is_minor=False))
    for _ in range(unemployed):
        population.append(Person(is_employed=False, is_retired=False, is_minor=False))
    for _ in range(retired):
        population.append(Person(is_employed=False, is_retired=True, is_minor=False))
    for _ in range(minors):
        population.append(Person(is_employed=False, is_retired=False, is_minor=True))
    return population

def initialize_companies(total_companies, services_pct, industry_pct, commerce_pct, population):
    companies = []
    services_count = int(total_companies * services_pct)
    industry_count = int(total_companies * industry_pct)
    commerce_count = int(total_companies * commerce_pct)

    # Distribuição de empregados entre as empresas
    employees_per_company = [len(population) // total_companies] * total_companies
    remaining_employees = len(population) % total_companies
    for i in range(remaining_employees):
        employees_per_company[i] += 1

    population_copy = population.copy()
    for _ in range(services_count):
        employees = random.sample(population_copy, employees_per_company.pop(0))
        companies.append(Company(sector='Services', employees=employees, initial_capital=random.randint(500000, 10000000)))
        population_copy = [person for person in population_copy if person not in employees]
    for _ in range(industry_count):
        employees = random.sample(population_copy, employees_per_company.pop(0))
        companies.append(Company(sector='Industry', employees=employees, initial_capital=random.randint(5000000, 100000000)))
        population_copy = [person for person in population_copy if person not in employees]
    for _ in range(commerce_count):
        employees = random.sample(population_copy, employees_per_company.pop(0))
        companies.append(Company(sector='Commerce', employees=employees, initial_capital=random.randint(900000, 50000000)))
        population_copy = [person for person in population_copy if person not in employees]

    return companies

def run_simulation(months, population, companies, state):

    total_salaries = 0
    total_pensions = 0
    total_income = 0
    people_failed = 0
    companies_failed = 0

    for month in range(months):
        total_consumption = 0
        total_taxes = 0
        total_capital = 0
        people_failed_this_month = 0
        companies_failed_this_month = 0
        
        # Companies pay salaries
        for company in companies:
            if company.capital <= 0:
                companies_failed += 1
                companies_failed_this_month += 1
            total_salaries = company.pay_salaries()
            total_taxes += company.collect_taxes()
            total_capital += company.capital

        for person in population:
            if person.wallet <= 0:
                people_failed += 1
                people_failed_this_month += 1
            total_consumption += person.consumption
                
        # Companies receive revenue from consumption
        for company in companies:
            company.receive_revenue(total_consumption / len(companies))
        
        print(f"Month {month+1}: Total Capital: {total_capital}, Total Taxes: {total_taxes}, Companies Failed: {companies_failed}, People Failed: {people_failed}")
        print(f"People Failed this Month: {people_failed_this_month}, Companies Failed this Month: {companies_failed_this_month}")
    
    # Generate final report
    generate_report(total_salaries, total_pensions, total_income, total_capital, total_taxes, state)

def generate_report(total_salaries, total_pensions, total_income, initial_capital, total_taxes, state):
        def calc_percentage_change(initial, final):
            return ((final - initial) / initial) * 100

        salaries_change = calc_percentage_change(state['initial_salaries'], total_salaries)
        pensions_change = calc_percentage_change(state['initial_pensions'], total_pensions)
        income_change = calc_percentage_change(state['initial_income'], total_income)
        initial_capital = calc_percentage_change(state['initial_capital'], initial_capital)
        taxes_change = calc_percentage_change(state['initial_taxes'], total_taxes)

        print("Final Report:")
        print(f"  Salaries Change: {salaries_change:.2f}%")
        print(f"  Pensions Change: {pensions_change:.2f}%")
        print(f"  Total Income Change: {income_change:.2f}%")
        print(f"  Capital Change: {initial_capital:.2f}%")
        print(f"  Taxes Change: {taxes_change:.2f}%")

# Parameters
total_population = math.floor(215_300_000 / 10000)
unemployed = math.floor(8_600_000 / 10000)
retired = math.floor(23_034_648 / 10000)
minors = math.floor(53_759_457 / 10000)
total_companies = math.floor(21_800_000 / 10000)
services_pct = 0.395
industry_pct = 0.208
commerce_pct = 0.193
months = 12 * 10

salary_range = (1000, 5000)
pension = 2000
taxes_rate = 0.2



# Initialization
population = initialize_population(total_population, unemployed, retired, minors)
companies = initialize_companies(total_companies, services_pct, industry_pct, commerce_pct, population)

initial_capital = 0
for company in companies:
    initial_capital += company.capital

# Initial state
state = {
    'initial_capital': initial_capital,
    'initial_salaries': (total_population - (unemployed + retired + minors)) * sum(salary_range) // 2,
    'initial_pensions': retired * pension,
    'initial_income': ((total_population - (unemployed + retired + minors)) * sum(salary_range)) // 2 + (retired * pension),
    'initial_consumption': (((total_population - (unemployed + retired + minors)) * sum(salary_range)) // 2 + (retired * pension)) * 0.7,
    'initial_taxes': (((total_population - (unemployed + retired + minors)) * sum(salary_range)) // 2 + (retired * pension)) * taxes_rate
}

print(f"Total Population: {total_population}")
print(f"Unemployed: {unemployed}")
print(f"Retired: {retired}")
print(f"Minors: {minors}" )
print(f"Total Companies: {total_companies}")
print(f"Services Percentage: {services_pct}")
print(f"Industry Percentage: {industry_pct}")
print(f"Commerce Percentage: {commerce_pct}")
print(f"Months: {months}")

print(f"initial_capital: {state['initial_capital']}")
print(f"initial_salaries: {state['initial_salaries']}")
print(f"initial_pensions: {state['initial_pensions']}")
print(f"initial_income: {state['initial_income']}")
print(f"initial_consumption: {state['initial_consumption']}")
print(f"initial_taxes: {state['initial_taxes']}")

# Run Simulation
run_simulation(months, population, companies, state)
