from src.order import Order  # circular


class User:
    def __init__(self, uid, name):
        self.uid = uid
        self.name = name

    def make_order(self, items):
        return Order.create_for(self, items)
