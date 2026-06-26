from src.calc import add_positive, safe_div, grade


def test_add_positive_happy():
    assert add_positive(2, 3) == 5
