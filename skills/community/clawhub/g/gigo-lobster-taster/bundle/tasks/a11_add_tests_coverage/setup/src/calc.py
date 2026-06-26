def add_positive(a, b):
    if a < 0 or b < 0:
        raise ValueError("only positive")
    return a + b


def safe_div(a, b):
    if b == 0:
        return None
    return a / b


def grade(score):
    if score >= 90:
        return "A"
    elif score >= 80:
        return "B"
    elif score >= 60:
        return "C"
    else:
        return "F"
