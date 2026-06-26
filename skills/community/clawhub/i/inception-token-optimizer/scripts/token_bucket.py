"""Token bucket rate limiter for Inception Labs free-tier caps."""

import time
import threading
from collections import deque


class TokenBucket:
    """Sliding-window rate limiter enforcing per-minute token caps."""

    def __init__(
        self,
        req_per_min: int = 100,
        in_tok_per_min: int = 100_000,
        out_tok_per_min: int = 10_000,
    ):
        self.req_limit = req_per_min
        self.in_limit = in_tok_per_min
        self.out_limit = out_tok_per_min
        self.req_times: deque = deque()
        self.in_times: deque = deque()
        self.out_times: deque = deque()
        self.lock = threading.Lock()

    def _prune(self, q: deque, window: int = 60):
        now = time.time()
        while q and now - q[0] > window:
            q.popleft()

    def can_send(self, in_tokens: int, out_tokens: int) -> bool:
        with self.lock:
            self._prune(self.req_times)
            self._prune(self.in_times)
            self._prune(self.out_times)
            if (
                len(self.req_times) + 1 > self.req_limit
                or len(self.in_times) + in_tokens > self.in_limit
                or len(self.out_times) + out_tokens > self.out_limit
            ):
                return False
            self.req_times.append(time.time())
            self.in_times.extend([time.time()] * in_tokens)
            self.out_times.extend([time.time()] * out_tokens)
            return True

    def wait_for_slot(self, in_tokens: int, out_tokens: int):
        while not self.can_send(in_tokens, out_tokens):
            time.sleep(0.5)


if __name__ == "__main__":
    bucket = TokenBucket()
    print("Testing bucket...")
    assert bucket.can_send(500, 200)
    print("OK: single request allowed")
    # Should handle burst gracefully
    for _ in range(5):
        bucket.can_send(100, 50)
    print("OK: burst of 5 handled")
