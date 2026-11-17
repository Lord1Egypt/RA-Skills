from decimal import Decimal, ROUND_FLOOR, ROUND_HALF_UP
D = Decimal
ZERO = D("0")

def dec(x):
    y = D(str(x))
    if not y.is_finite():
        raise ValueError('non-finite decimal')
    return y

def fee(q, p):
    return (q * D('0.07') * p * (1 - p)).quantize(D('0.00001'), rounding=ROUND_HALF_UP)

def floor_tick(p, tick):
    return (p / tick).to_integral_value(rounding=ROUND_FLOOR) * tick