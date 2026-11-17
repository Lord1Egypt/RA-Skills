"""Mechanically extracted from the verified paper prototype; single-writer EngineState."""
from datetime import datetime, timezone
from pm_predict.domain.money import D, ZERO, dec, fee, floor_tick
from pm_predict.domain.models import Window, Order, Fill, SIDES, TERMINAL
import pm_predict.domain.invariants as domain_invariants
import pm_predict.domain.queries as domain_queries
import pm_predict.execution.orders as execution_orders
def confirm(self, fill_id, now, success=True):
    self._time(now)
    f = self.fills[fill_id]
    if f.status != 'MATCHED':
        if (f.status == 'CONFIRMED') != success:
            self.halted = 'conflicting final fill status'
            raise ValueError(self.halted)
        return
    o = self.orders[f.order]
    w = self.windows[o.market]
    if success:
        f.status = 'CONFIRMED'
        cost = f.qty * f.price + f.fee
        self.cash -= cost
        w.qty[o.side] += f.qty
        w.cost[o.side] += cost
    else:
        f.status, o.status = ('FAILED', 'UNKNOWN')
        execution_orders.block(self, w, 'fill failed; reconcile order before releasing reservation')
    self._log('SYNTHETIC_CONFIRMED' if success else 'SYNTHETIC_FAILED', fill=fill_id)
    domain_invariants.check(self)

def merge(self, w):
    q = min(w.qty.values())
    if q and (not w.chain) and (not w.merge_failed):
        w.chain = ('MERGE', q)
        self._intent('PAPER_MERGE', market=w.id, qty=str(q))

def settle(self, market, winner, now):
    self._time(now)
    w = self.windows[market]
    if now < (w.start + 900) * 1000 or winner not in SIDES:
        raise ValueError('invalid resolution')
    if w.winner is not None and w.winner != winner:
        raise ValueError('conflicting resolution')
    w.winner = winner
    if not domain_queries.active(self, market) and (not domain_queries.pending(self, market)) and (not w.chain) and (not w.closed):
        w.chain = ('REDEEM', w.qty[winner])
        self._intent('PAPER_REDEEM', market=market, winner=winner, qty=str(w.qty[winner]))

def realize(self, w, value):
    self.realized += value
    w.realized += value
    day = datetime.fromtimestamp(self.now / 1000, timezone.utc).date().isoformat()
    self.daily[day] = self.daily.get(day, ZERO) + value
    if self.realized <= -20:
        self.halted = 'cumulative realized loss reached 20 USD'
        for other in self.windows.values():
            execution_orders.cancel(self, other, self.halted)

def chain_result(self, market, now, success, operation):
    self._time(now)
    w = self.windows[market]
    if not w.chain or operation != w.chain[0]:
        raise ValueError('unknown chain operation; replay receipts by unique event ID')
    kind, q = w.chain
    w.chain = None
    if not success:
        if kind == 'MERGE':
            w.merge_failed = True
        self._log('PAPER_CHAIN_FAILED', market=market, operation=kind)
        return
    if kind == 'MERGE':
        removed = ZERO
        for side in SIDES:
            c = w.cost[side] * q / w.qty[side]
            removed += c
            w.cost[side] -= c
            w.qty[side] -= q
        self.cash += q
        realize(self, w, q - removed)
    else:
        self.cash += q
        realize(self, w, q - sum(w.cost.values()))
        w.qty, w.cost = (dict.fromkeys(SIDES, ZERO), dict.fromkeys(SIDES, ZERO))
        w.closed = True
        if w.realized < 0:
            self.loss_streak += 1
        elif w.realized > 0:
            self.loss_streak = 0
        if self.loss_streak >= 8:
            self.pause_until = now + 24 * 3600 * 1000
    self._log('PAPER_CHAIN_CONFIRMED', market=market, operation=kind, credited=str(q))
    domain_invariants.check(self)
