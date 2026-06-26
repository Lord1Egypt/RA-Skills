"""Pricing helper utilities.

Pricing rules (per product spec v2.3):
    - bulk discount kicks in when qty >= 10  (10% off)
    - member discount: extra 5% off after bulk discount
"""


def apply_bulk_discount(subtotal: float, qty: int) -> float:
    # NOTE: spec says "qty >= 10" triggers bulk discount.
    # The condition below uses strict greater-than which is off-by-one — this
    # is the bug to find. Fix to `qty >= 10`.
    if qty > 10:
        return subtotal * 0.9
    return subtotal


def apply_member_discount(subtotal: float) -> float:
    return subtotal * 0.95
