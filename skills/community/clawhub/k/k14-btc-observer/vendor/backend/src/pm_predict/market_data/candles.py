import math
from pm_predict.strategy.indicators import Bar

class TradeBars:
    """Normalized contiguous Binance trade IDs; gaps require external backfill/reset.

    Arrival order is not silently sorted. The first partially observed bar is invalid.
    A late trade cannot rewrite a bar already used for a decision.
    """

    def __init__(self):
        self.current = None
        self.last_id = None
        self.last_ms = None
        self.valid = False
        self.blocked = False
        self.last_trade = None

    def push(self, trade_id, ts_ms, price):
        if self.blocked:
            raise ValueError('stream requires backfill/reset')
        if not math.isfinite(price) or price <= 0:
            self.blocked = True
            raise ValueError('invalid trade')
        if self.last_id == trade_id:
            if self.last_trade == (ts_ms, price):
                return None
            self.blocked = True
            raise ValueError('conflicting duplicate trade ID')
        if self.last_id is not None and (trade_id != self.last_id + 1 or ts_ms < self.last_ms):
            self.blocked = True
            raise ValueError('trade gap/out-of-order; no guessed candle')
        start = ts_ms // 1000 // 900 * 900
        closed = None
        if self.current is None:
            self.current = Bar(start, price, price, price)
        elif start > self.current.start:
            if start != self.current.start + 900:
                self.blocked = True
                raise ValueError('missing candle')
            if self.valid:
                closed = self.current
            self.current = Bar(start, price, price, price)
            self.valid = True
        else:
            b = self.current
            self.current = Bar(start, max(b.high, price), min(b.low, price), price)
        self.last_id, self.last_ms, self.last_trade = (trade_id, ts_ms, (ts_ms, price))
        return closed
