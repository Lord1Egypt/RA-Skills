from src.calc import add


def test_add_positive():
    assert add(2, 3) == 5


def test_add_negative():
    assert add(-1, -4) == -5


def test_add_zero():
    assert add(0, 0) == 0


def test_add_floats():
    assert add(1.5, 2.5) == 4.0


def test_add_large():
    assert add(10**6, 10**6) == 2 * 10**6
