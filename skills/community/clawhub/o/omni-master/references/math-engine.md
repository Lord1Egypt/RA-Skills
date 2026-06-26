# Mathematics & Calculation Engine

Complete math capabilities — from arithmetic to statistics, finance math, geometry, and unit conversions.

---

## 1. Arithmetic & Algebra

### Basic Operations
```python
# Python as calculator
2 + 3    # 5 (addition)
10 - 4   # 6 (subtraction)
3 * 7    # 21 (multiplication)
15 / 4   # 3.75 (division)
15 // 4  # 3 (floor division)
15 % 4   # 3 (modulus)
2 ** 10  # 1024 (exponentiation)
```

### Order of Operations
PEMDAS: Parentheses → Exponents → Multiplication/Division → Addition/Subtraction

### Algebra
```python
# Solve equations
from sympy import symbols, solve, Eq
x = symbols('x')
solve(Eq(x**2 - 5*x + 6, 0), x)  # [2, 3]
solve(2*x + 5 - 11, x)            # [3]
```

### Linear Algebra
```python
import numpy as np

# Matrix operations
A = np.array([[1, 2], [3, 4]])
B = np.array([[5, 6], [7, 8]])
A @ B          # Matrix multiplication
np.linalg.inv(A)  # Inverse
np.linalg.det(A)  # Determinant
np.linalg.eig(A)  # Eigenvalues/vectors
```

---

## 2. Calculus

### Derivatives
```python
from sympy import diff, symbols
x = symbols('x')
diff(x**3 + 2*x, x)        # 3*x**2 + 2
diff(sin(x) * exp(x), x)    # exp(x)*cos(x) + exp(x)*sin(x)
```

### Integrals
```python
from sympy import integrate
integrate(x**2, x)                    # x**3/3
integrate(x**2, (x, 0, 1))           # 1/3 (definite)
integrate(exp(-x**2), (x, -oo, oo))  # sqrt(pi)
```

### Limits
```python
from sympy import limit
limit(sin(x)/x, x, 0)    # 1
limit((1 + 1/x)**x, x, oo)  # E (Euler's number)
```

---

## 3. Statistics & Probability

### Descriptive Statistics
```python
import numpy as np
from scipy import stats

data = [23, 45, 12, 67, 34, 89, 56, 78, 43, 21]

np.mean(data)           # Mean (average)
np.median(data)         # Median (middle)
np.std(data)            # Standard deviation
np.var(data)            # Variance
np.percentile(data, 25) # 25th percentile (Q1)
np.percentile(data, 75) # 75th percentile (Q3)
stats.mode(data)        # Mode (most frequent)
```

### Probability Distributions
```python
from scipy import stats

# Normal distribution
dist = stats.norm(loc=0, scale=1)  # mean=0, std=1
dist.pdf(0)     # Probability density at 0
dist.cdf(1.96)  # Cumulative probability
dist.ppf(0.95)  # Inverse CDF (quantile)

# Confidence interval
data = [23, 45, 12, 67, 34]
ci = stats.t.interval(0.95, len(data)-1, 
                       loc=np.mean(data), 
                       scale=stats.sem(data))
```

### Hypothesis Testing
```python
from scipy import stats

# t-test (are two groups different?)
group1 = [23, 45, 12, 67, 34]
group2 = [34, 56, 23, 78, 45]
t_stat, p_value = stats.ttest_ind(group1, group2)

# If p < 0.05 → significant difference
# If p >= 0.05 → no significant difference
```

### Regression
```python
from scipy import stats
import numpy as np

x = np.array([1, 2, 3, 4, 5])
y = np.array([2.1, 4.0, 5.9, 8.1, 10.0])

slope, intercept, r, p, se = stats.linregress(x, y)
# y = slope * x + intercept
# r = correlation coefficient
```

---

## 4. Financial Mathematics

### Compound Interest
```python
def compound_interest(principal, rate, times_per_year, years):
    return principal * (1 + rate/times_per_year)**(times_per_year * years)

# $1000 at 5% annually for 10 years
compound_interest(1000, 0.05, 1, 10)  # $1628.89
```

### Loan Payment
```python
def monthly_payment(principal, annual_rate, years):
    r = annual_rate / 12
    n = years * 12
    return principal * (r * (1+r)**n) / ((1+r)**n - 1)

# $200k mortgage at 6% for 30 years
monthly_payment(200000, 0.06, 30)  # $1199.10
```

### ROI
```python
def roi(gain, cost):
    return (gain - cost) / cost * 100

roi(15000, 10000)  # 50% return
```

### CAGR (Compound Annual Growth Rate)
```python
def cagr(beginning, ending, years):
    return (ending / beginning)**(1/years) - 1

cagr(1000, 2000, 5)  # 14.87% per year
```

---

## 5. Geometry & Trigonometry

### Basic Geometry
```python
import math

# Circle
r = 5
area = math.pi * r**2
circumference = 2 * math.pi * r

# Triangle (Heron's formula)
def triangle_area(a, b, c):
    s = (a + b + c) / 2
    return math.sqrt(s*(s-a)*(s-b)*(s-c))

# Distance between points
def distance(x1, y1, x2, y2):
    return math.sqrt((x2-x1)**2 + (y2-y1)**2)
```

### Trigonometry
```python
import math

math.sin(math.radians(30))   # 0.5
math.cos(math.radians(60))   # 0.5
math.tan(math.radians(45))   # 1.0
math.asin(0.5)               # radians → degrees: math.degrees()
```

---

## 6. Unit Conversions

### Common Conversions
```python
# Temperature
def c_to_f(c): return c * 9/5 + 32
def f_to_c(f): return (f - 32) * 5/9
def c_to_k(c): return c + 273.15

# Distance
miles_to_km = 1.60934
feet_to_m = 0.3048
inches_to_cm = 2.54

# Weight
lbs_to_kg = 0.453592
oz_to_g = 28.3495

# Data
def bytes_to_human(b):
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if b < 1024:
            return f"{b:.1f} {unit}"
        b /= 1024
    return f"{b:.1f} PB"
```

### Quick Reference
| From | To | Multiply by |
|---|---|---|
| Miles | Km | 1.609 |
| Pounds | Kg | 0.454 |
| Fahrenheit | Celsius | (F-32)×5/9 |
| Inches | Cm | 2.54 |
| Gallons (US) | Liters | 3.785 |
| Acres | Hectares | 0.405 |

---

## 7. Number Theory & Combinatorics

### Primes & Factors
```python
def is_prime(n):
    if n < 2: return False
    for i in range(2, int(n**0.5)+1):
        if n % i == 0: return False
    return True

def factors(n):
    return [i for i in range(1, n+1) if n % i == 0]
```

### Permutations & Combinations
```python
from math import perm, comb
perm(5, 3)   # 60 (5P3: arrange 3 from 5)
comb(5, 3)   # 10 (5C3: choose 3 from 5)
```

### Fibonacci
```python
def fibonacci(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a
```

### GCD & LCM
```python
from math import gcd, lcm
gcd(12, 8)   # 4
lcm(12, 8)   # 24
```
