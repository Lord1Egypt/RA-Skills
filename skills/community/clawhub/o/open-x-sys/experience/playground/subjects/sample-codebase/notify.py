"""Customer notification (simulated provider)."""

import time

NOTIFY_SECONDS = 0.05


class ProviderDown(Exception):
    pass


class Notifier:
    def __init__(self, seconds=NOTIFY_SECONDS, fail_first=0):
        self.seconds = seconds
        self.calls = 0
        self._fail_first = fail_first
        self.sent = []

    def send(self, order_id, customer):
        """Send a confirmation. Blocks for the provider's latency."""
        self.calls += 1
        time.sleep(self.seconds)
        if self.calls <= self._fail_first:
            raise ProviderDown("notification provider unavailable")
        self.sent.append((order_id, customer))
