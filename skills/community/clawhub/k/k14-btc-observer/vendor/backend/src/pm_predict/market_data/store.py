"""Mechanically extracted from the verified paper prototype; single-writer EngineState."""
from datetime import datetime, timezone
from pm_predict.domain.money import D, ZERO, dec, fee, floor_tick
from pm_predict.domain.models import Window, Order, Fill, SIDES, TERMINAL
import pm_predict.execution.orders as execution_orders
def book(self, market, side, seq, source_ms, receive_ms, bid, asks, tick=None):
    self._time(receive_ms)
    w = self.windows[market]
    if side not in SIDES:
        raise ValueError('unknown outcome')
    levels = [(dec(p), dec(q)) for p, q in asks]
    b = dec(bid)
    if not levels or not ZERO <= b < 1 or any((not ZERO < p < 1 or q <= 0 for p, q in levels)):
        execution_orders.block(self, w, 'invalid/empty book')
        return
    if levels != sorted(levels) or len(set((p for p, q in levels))) != len(levels) or b >= levels[0][0]:
        execution_orders.block(self, w, 'crossed/unsorted book')
        return
    if tick is not None and dec(tick) != w.tick:
        execution_orders.block(self, w, 'tick changed: require a new validated window')
        return
    if any((p % w.tick for p, q in levels)) or b % w.tick:
        execution_orders.block(self, w, 'off-tick book')
        return
    old = w.books.get(side)
    record = (seq, source_ms, b, levels)
    if old and record == old:
        return
    if old and (seq != old[0] + 1 or source_ms < old[1]):
        execution_orders.block(self, w, 'normalized capture sequence gap/conflict')
        return
    if not 0 <= receive_ms - source_ms <= 2000:
        execution_orders.block(self, w, 'stale/future book')
        return
    w.books[side] = record

def price(self, market, spot, sigma, source_ms, receive_ms):
    self._time(receive_ms)
    w = self.windows[market]
    if source_ms < w.price_ms or not 0 <= receive_ms - source_ms <= 2000:
        execution_orders.block(self, w, 'late/stale/future price')
        return
    w.spot, w.sigma, w.price_ms = (float(spot), float(sigma), source_ms)

def health(self, market, now, clock_offset_ms=0, reconciled=False, connected=False, maintenance=False):
    self._time(now)
    w = self.windows[market]
    w.clock_ms, w.maintenance = (float(clock_offset_ms), maintenance)
    if not connected or not reconciled:
        execution_orders.block(self, w, 'disconnected/unreconciled')
        return
    w.health_ms = now

def fresh(self, w):
    stamps = [w.health_ms, w.price_ms] + [w.books[s][1] if s in w.books else -1 for s in SIDES]
    return abs(w.clock_ms) < 50 and all((0 <= self.now - t <= 2000 for t in stamps))
