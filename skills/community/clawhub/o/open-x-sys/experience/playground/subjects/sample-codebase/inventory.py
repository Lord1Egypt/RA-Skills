"""Stock reservation."""

import threading


class OutOfStock(Exception):
    pass


class Inventory:
    def __init__(self, stock):
        self._stock = dict(stock)
        # One lock for the whole inventory keeps the counts consistent.
        self.lock = threading.Lock()

    def available(self, sku):
        return self._stock.get(sku, 0)

    def reserve(self, sku, quantity):
        """Reserve stock. The caller must hold self.lock."""
        if self._stock.get(sku, 0) < quantity:
            raise OutOfStock(sku)
        self._stock[sku] -= quantity
