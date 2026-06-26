"""Pricing engine entry point."""
from .utils import apply_bulk_discount, apply_member_discount


def calculate_price(unit_price: float, qty: int, is_member: bool) -> float:
    subtotal = unit_price * qty
    subtotal = apply_bulk_discount(subtotal, qty)
    if is_member:
        subtotal = apply_member_discount(subtotal)
    return round(subtotal, 2)
