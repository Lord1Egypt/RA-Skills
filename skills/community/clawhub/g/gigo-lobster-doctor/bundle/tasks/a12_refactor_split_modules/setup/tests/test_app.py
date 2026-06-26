from src.users import User
from src.orders import Order
from src.invoices import Invoice


def test_user_create():
    u = User("alice", "a@x.com")
    assert u.name == "alice"
    assert u.email == "a@x.com"
    assert u.id >= 1


def test_order_create():
    u = User("bob", "b@x.com")
    o = Order(u, [{"name": "x", "price": 10.0, "qty": 2}])
    assert o.subtotal() == 20.0
    o.add_item({"name": "y", "price": 5.0, "qty": 1})
    assert o.subtotal() == 25.0


def test_invoice_total():
    u = User("carol", "c@x.com")
    o = Order(u, [{"name": "x", "price": 100.0, "qty": 1}])
    inv = Invoice(o, tax_rate=0.1)
    assert inv.total() == 110.0
