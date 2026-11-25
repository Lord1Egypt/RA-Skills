import unittest

from inventory import Inventory
from notify import Notifier
from orders import OrderService


def make_service(stock, fail_first=0):
    inventory = Inventory(stock)
    notifier = Notifier(seconds=0.001, fail_first=fail_first)
    service = OrderService(inventory, notifier)
    service.start()
    return service, inventory, notifier


class OrderTests(unittest.TestCase):
    def test_orders_are_processed(self):
        service, inventory, notifier = make_service({"mug": 100})
        for i in range(8):
            service.place(i, "customer-%d" % i, "mug", 1)
        service.wait()
        self.assertEqual(sorted(service.done), list(range(8)))
        self.assertEqual(inventory.available("mug"), 92)
        self.assertEqual(len(notifier.sent), 8)

    def test_out_of_stock_fails(self):
        service, inventory, notifier = make_service({"mug": 1})
        service.place(1, "ana", "mug", 2)
        service.wait()
        self.assertEqual(service.failed, [1])
        self.assertEqual(notifier.sent, [])

    def test_order_succeeds_after_provider_recovers(self):
        service, inventory, notifier = make_service({"mug": 10}, fail_first=1)
        service.place(1, "ana", "mug", 1)
        service.wait()
        self.assertEqual(service.done, [1])
        self.assertEqual(len(notifier.sent), 1)


if __name__ == "__main__":
    unittest.main()
