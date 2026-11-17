"""Causal features for the paper-only B prototype. No network or credentials."""
from collections import deque
from dataclasses import dataclass
from datetime import datetime, timezone
import math

@dataclass(frozen=True)
class Bar:
    start: int
    high: float
    low: float
    close: float

def k14(bars, window_start):
    if len(bars) < 14:
        raise ValueError('14 completed bars required')
    rows = bars[-14:]
    for i, b in enumerate(rows):
        if b.start != window_start - (14 - i) * 900:
            raise ValueError('missing/out-of-order/unclosed bar')
        if not all((math.isfinite(x) and x > 0 for x in (b.high, b.low, b.close))):
            raise ValueError('invalid OHLC')
        if not b.low <= b.close <= b.high:
            raise ValueError('invalid OHLC range')
    hh, ll = (max((b.high for b in rows)), min((b.low for b in rows)))
    return 0.0 if hh == ll else 2 * (rows[-1].close - ll) / (hh - ll) - 1

def signal(value, thresholds, window_start):
    month = datetime.fromtimestamp(window_start, timezone.utc).strftime('%Y-%m')
    if thresholds.get('month') != month:
        raise ValueError('threshold month mismatch')
    if thresholds.get('signal') != 'K14' or thresholds.get('q') != 0.05:
        raise ValueError('not the frozen B threshold file')
    lo, hi = (thresholds['lower'], thresholds['upper'])
    if not -1 <= lo < hi <= 1 or not math.isfinite(value):
        raise ValueError('invalid signal/threshold')
    return 'Up' if value < lo else 'Down' if value > hi else None

def fair_up(spot, ptb, sigma, seconds_to_end):
    if not all((math.isfinite(x) and x > 0 for x in (spot, ptb, sigma))):
        return None
    if not 60 < seconds_to_end <= 900:
        return None
    tau = (seconds_to_end - 60) / 60 + 1 / 3
    return 0.5 * (1 + math.erf(math.log(spot / ptb) / (sigma * math.sqrt(2 * tau))))

class Volatility:
    """O(1) rolling first/second moments; one-minute close timestamps must be contiguous."""

    def __init__(self):
        self.returns = deque()
        self.total = self.squares = 0.0
        self.last = None

    def push(self, minute_start, close):
        if not math.isfinite(close) or close <= 0 or minute_start % 60:
            raise ValueError('invalid minute close')
        if self.last is not None:
            t, p = self.last
            if minute_start != t + 60:
                raise ValueError('minute gap; backfill before using volatility')
            r = math.log(close / p)
            if len(self.returns) == 60:
                old = self.returns.popleft()
                self.total -= old
                self.squares -= old * old
            self.returns.append(r)
            self.total += r
            self.squares += r * r
        self.last = (minute_start, close)

    def sigma(self):
        n = len(self.returns)
        if n < 50:
            return None
        return math.sqrt(max(0, (self.squares - self.total * self.total / n) / (n - 1)))
