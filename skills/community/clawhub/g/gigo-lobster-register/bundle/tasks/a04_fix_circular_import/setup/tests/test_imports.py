def test_import_user():
    from src.user import User
    u = User(1, "alice")
    assert u.uid == 1


def test_import_order():
    from src.order import Order
    o = Order(None, [])
    assert o.items == []


def test_create_order_with_user():
    from src.user import User
    from src.order import Order
    u = User(2, "bob")
    o = u.make_order(["x"])
    assert isinstance(o, Order)
    assert o.user is u
    assert o.items == ["x"]
