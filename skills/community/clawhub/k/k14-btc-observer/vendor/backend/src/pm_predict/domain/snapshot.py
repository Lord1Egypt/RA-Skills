"""Mechanically extracted from the verified paper prototype; single-writer EngineState."""
from datetime import datetime, timezone
from pm_predict.domain.money import D, ZERO, dec, fee, floor_tick
from pm_predict.domain.models import Window, Order, Fill, SIDES, TERMINAL
import pm_predict.domain.invariants as domain_invariants
import pm_predict.domain.queries as domain_queries
def summary(self):
    domain_invariants.check(self)
    return {'mode': 'OFFLINE_PAPER', 'cash': str(self.cash), 'reserved': str(domain_queries.reserve(self)), 'realized_synthetic_pnl': str(self.realized), 'halted': self.halted, 'order_intents': len(self.orders), 'synthetic_fills': len(self.fills), 'actual_fill_probability': 'UNKNOWN', 'exchange_order_latency': 'NOT_MEASURED', 'actual_strategy_profit': 'UNKNOWN', 'windows': {k: {'k14': w.k, 'side': w.side, 'blocked': w.blocked, 'closed': w.closed, 'qty': {s: str(v) for s, v in w.qty.items()}, 'realized': str(w.realized)} for k, w in self.windows.items()}}
