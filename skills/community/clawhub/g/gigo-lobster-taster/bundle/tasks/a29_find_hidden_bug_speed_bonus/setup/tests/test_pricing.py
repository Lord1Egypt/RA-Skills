import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.pricing import calculate_price


def test_basic_price():
    assert calculate_price(10.0, 2, False) == 20.0


def test_no_discount():
    # qty=9 < 10, no bulk discount
    assert calculate_price(10.0, 9, False) == 90.0


def test_member_discount():
    # qty=2, member only — 20 * 0.95
    assert calculate_price(10.0, 2, True) == 19.0


def test_bulk_discount_threshold():
    # qty=10 must trigger bulk (10% off): 100 * 0.9 = 90.0
    assert calculate_price(10.0, 10, False) == 90.0


def test_bulk_discount_edge():
    # qty=10 + member: 100 * 0.9 * 0.95 = 85.5
    assert calculate_price(10.0, 10, True) == 85.5
