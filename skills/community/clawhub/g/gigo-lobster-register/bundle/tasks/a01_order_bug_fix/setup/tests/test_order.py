from src.order import calculate_total


def test_basic_total():
    items = [{"name": "a", "price": 10.0, "qty": 2}]
    assert calculate_total(items, 0, 0) == 20.0


def test_total_with_discount():
    items = [{"name": "a", "price": 100.0, "qty": 1}]
    assert calculate_total(items, 0.1, 0) == 90.0


def test_total_with_tax():
    items = [{"name": "a", "price": 100.0, "qty": 1}]
    assert abs(calculate_total(items, 0, 0.13) - 113.0) < 1e-6
