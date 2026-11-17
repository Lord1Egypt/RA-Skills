"""Mechanically extracted from the verified paper prototype; single-writer EngineState."""
from datetime import datetime, timezone
from pm_predict.domain.money import D, ZERO, dec, fee, floor_tick
from pm_predict.domain.models import Window, Order, Fill, SIDES, TERMINAL
def filled(self, order):
    return sum((f.qty for f in self.fills.values() if f.order == order and f.status != 'FAILED'), ZERO)

def pending(self, market):
    return any((f.status == 'MATCHED' and self.orders[f.order].market == market for f in self.fills.values()))

def active(self, market, kind=None):
    return [o for o in self.orders.values() if o.market == market and o.status not in TERMINAL and (kind is None or o.kind == kind)]

def reserve(self):
    value = ZERO
    for o in self.orders.values():
        remaining = max(ZERO, o.qty - filled(self, o.id)) if o.status not in TERMINAL else ZERO
        value += remaining * o.price
        if o.kind == 'HEDGE' and remaining:
            value += fee(remaining, o.price) + D('0.00001') * remaining
    value += sum((f.qty * f.price + f.fee for f in self.fills.values() if f.status == 'MATCHED'), ZERO)
    return value

def risk(self):
    inventory = sum((max(ZERO, sum(w.cost.values()) - min(w.qty.values())) for w in self.windows.values()), ZERO)
    return inventory + reserve(self)

def occupied(self, w):
    return bool(sum(w.qty.values()) or active(self, w.id) or pending(self, w.id) or w.chain)
