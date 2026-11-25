"""Order queue and workers."""

import queue
import threading

from inventory import OutOfStock
from notify import ProviderDown

WORKERS = 4
MAX_ATTEMPTS = 3
BACKOFF_BASE_SECONDS = 0.5


class OrderService:
    def __init__(self, inventory, notifier, workers=WORKERS):
        self.inventory = inventory
        self.notifier = notifier
        self.queue = queue.Queue()
        self.done = []
        self.failed = []
        self._threads = [
            threading.Thread(target=self._work, daemon=True) for _ in range(workers)
        ]

    def start(self):
        for thread in self._threads:
            thread.start()

    def place(self, order_id, customer, sku, quantity):
        self.queue.put((order_id, customer, sku, quantity))

    def wait(self):
        self.queue.join()

    def _work(self):
        while True:
            order = self.queue.get()
            try:
                self._process(order)
            finally:
                self.queue.task_done()

    def _process(self, order):
        order_id, customer, sku, quantity = order
        for attempt in range(1, MAX_ATTEMPTS + 1):
            try:
                with self.inventory.lock:
                    self.inventory.reserve(sku, quantity)
                    self.notifier.send(order_id, customer)
                self.done.append(order_id)
                return
            except ProviderDown:
                continue
            except OutOfStock:
                break
        self.failed.append(order_id)
