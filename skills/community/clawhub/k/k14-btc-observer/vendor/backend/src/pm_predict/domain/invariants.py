"""Mechanically extracted from the verified paper prototype; single-writer EngineState."""
from datetime import datetime, timezone
from pm_predict.domain.money import D, ZERO, dec, fee, floor_tick
from pm_predict.domain.models import Window, Order, Fill, SIDES, TERMINAL
import pm_predict.domain.queries as domain_queries
def check(self):
    cost = sum((sum(w.cost.values()) for w in self.windows.values()), ZERO)
    assert abs(self.cash + cost - self.initial - self.realized) < D('0.00000001'), 'cash/basis conservation'
    assert self.cash >= 0 and self.cash - domain_queries.reserve(self) >= 0, 'overspent reserved cash'
    for w in self.windows.values():
        assert all((q >= 0 for q in w.qty.values())), 'negative inventory'
        used = sum((domain_queries.filled(self, o.id) for o in self.orders.values() if o.market == w.id and o.kind == 'ENTRY'), ZERO)
        assert used <= 5, 'entry exceeds five shares'
