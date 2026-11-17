"""Mechanically extracted from the verified paper prototype; single-writer EngineState."""
from datetime import datetime, timezone
from pm_predict.domain.money import D, ZERO, dec, fee, floor_tick
from pm_predict.domain.models import Window, Order, Fill, SIDES, TERMINAL
import pm_predict.domain.invariants as domain_invariants
import pm_predict.domain.queries as domain_queries
import pm_predict.risk.policy as risk_policy
def send(self, w, side, qty, p, kind):
    if qty < w.min_qty or qty % D('0.01') or (not ZERO < p <= D('0.50')) or p % w.tick:
        self._log('SKIP_ORDER', market=w.id, reason='price/size hard gate')
        return None
    extra = qty * p + (fee(qty, p) + D('0.00001') * qty if kind == 'HEDGE' else ZERO)
    reason = risk_policy.budget(self, w, extra)
    if reason:
        self._log('SKIP_ORDER', market=w.id, reason=reason)
        return None
    oid = f'P{len(self.orders) + 1:04d}'
    self.orders[oid] = Order(oid, w.id, side, qty, p, kind, self.now)
    self._intent('PAPER_ORDER', order=oid, market=w.id, side=side, qty=str(qty), price=str(p), order_type='GTC' if kind == 'ENTRY' else 'FOK', post_only=kind == 'ENTRY')
    return oid

def cancel(self, w, reason):
    for o in domain_queries.active(self, w.id, 'ENTRY'):
        if o.status not in ('CANCEL_PENDING', 'CANCELLED_WAIT_RECONCILE'):
            o.status = 'CANCEL_PENDING'
            o.cancel_ms = self.now
            self._intent('CANCEL', order=o.id, reason=reason)

def block(self, w, reason):
    w.blocked = reason
    cancel(self, w, reason)
    self._log('WINDOW_BLOCKED', market=w.id, reason=reason)

def ack(self, order, now, accepted=True):
    self._time(now)
    o = self.orders[order]
    if not accepted:
        if domain_queries.filled(self, order):
            block(self, self.windows[o.market], 'rejection conflicts with observed fill')
            return
        o.status = 'REJECTED'
    elif o.status == 'SENT':
        o.status = 'LIVE'
    self._log('ACK', order=order, accepted=accepted)

def cancel_ack(self, order, now):
    self._time(now)
    o = self.orders[order]
    if o.status not in TERMINAL:
        o.status = 'CANCELLED_WAIT_RECONCILE'
    self._log('CANCEL_ACK_WAIT_FILL_FENCE', order=order)

def reconcile(self, order, now, final_filled):
    """Normalized terminal order + trade-history fence, not merely a cancel HTTP reply."""
    self._time(now)
    o = self.orders[order]
    q = dec(final_filled)
    if o.status not in ('CANCELLED_WAIT_RECONCILE', 'UNKNOWN') or q != domain_queries.filled(self, order):
        block(self, self.windows[o.market], 'terminal order / trade ledger mismatch')
        return
    o.final_total, o.status = (q, 'CANCELLED')
    self._log('RECONCILED', order=order, final_filled=str(q))
    domain_invariants.check(self)

def fill(self, fill_id, order, qty, price, now, fee_usd='0', synthetic=False):
    self._time(now)
    if not synthetic:
        raise ValueError('offline engine requires an explicitly SYNTHETIC fill receipt')
    o = self.orders[order]
    q, p, f = (dec(qty), dec(price), dec(fee_usd))
    if fill_id in self.fills:
        old = self.fills[fill_id]
        if (old.order, old.qty, old.price, old.fee) != (order, q, p, f):
            self.halted = 'conflicting duplicate fill'
            raise ValueError(self.halted)
        return
    expected = ZERO if o.kind == 'ENTRY' else fee(q, p)
    if q <= 0 or not ZERO < p <= o.price or f != expected or (domain_queries.filled(self, order) + q > o.qty):
        self.halted = 'invalid fill receipt; reconciliation required'
        raise ValueError(self.halted)
    if o.status == 'REJECTED' or o.final_total is not None:
        self.halted = 'fill contradicts final reconciliation; raw event must be investigated'
        raise ValueError(self.halted)
    self.fills[fill_id] = Fill(fill_id, order, q, p, f)
    if domain_queries.filled(self, order) == o.qty:
        o.status = 'FILLED'
    self._log('SYNTHETIC_MATCHED', fill=fill_id, order=order, qty=str(q), price=str(p), fee=str(f))
    domain_invariants.check(self)
