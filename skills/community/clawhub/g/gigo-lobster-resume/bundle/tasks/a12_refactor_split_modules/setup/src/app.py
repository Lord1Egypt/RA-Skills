"""Monolithic app — needs splitting into users / orders / invoices."""
from datetime import datetime


# ---------- USERS ----------
class User:
    _next_id = 1

    def __init__(self, name, email):
        self.id = User._next_id
        User._next_id += 1
        self.name = name
        self.email = email
        self.created_at = datetime.utcnow()

    def __repr__(self):
        return f"<User {self.id} {self.name}>"


def find_user(users, uid):
    for u in users:
        if u.id == uid:
            return u
    return None


def list_user_emails(users):
    return [u.email for u in users]


def rename_user(user, new_name):
    user.name = new_name
    return user


# ---------- ORDERS ----------
class Order:
    _next_id = 1

    def __init__(self, user, items):
        self.id = Order._next_id
        Order._next_id += 1
        self.user = user
        self.items = items  # list of {"name", "price", "qty"}
        self.created_at = datetime.utcnow()

    def subtotal(self):
        return sum(it["price"] * it["qty"] for it in self.items)

    def add_item(self, item):
        self.items.append(item)


def total_orders_for_user(orders, user):
    return [o for o in orders if o.user is user]


def order_count(orders):
    return len(orders)


def biggest_order(orders):
    if not orders:
        return None
    return max(orders, key=lambda o: o.subtotal())


# ---------- INVOICES ----------
class Invoice:
    _next_id = 1

    def __init__(self, order, tax_rate=0.13):
        self.id = Invoice._next_id
        Invoice._next_id += 1
        self.order = order
        self.tax_rate = tax_rate
        self.issued_at = datetime.utcnow()

    def total(self):
        sub = self.order.subtotal()
        return round(sub * (1 + self.tax_rate), 2)

    def line_items(self):
        return [
            {"name": it["name"], "amount": it["price"] * it["qty"]}
            for it in self.order.items
        ]


def issue_invoices(orders, tax_rate=0.13):
    return [Invoice(o, tax_rate) for o in orders]


def total_revenue(invoices):
    return sum(inv.total() for inv in invoices)
