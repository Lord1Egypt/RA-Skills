from src.calc import add, concat, average


def test_add():
    assert add(2, 3) == 5


def test_concat():
    assert concat(["a", "b", "c"], "-") == "a-b-c"


def test_average():
    assert abs(average([1.0, 2.0, 3.0]) - 2.0) < 1e-9
    assert average([]) == 0.0
