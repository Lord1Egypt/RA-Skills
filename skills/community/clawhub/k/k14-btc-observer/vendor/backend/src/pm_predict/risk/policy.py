"""Mechanically extracted from the verified paper prototype; single-writer EngineState."""
from datetime import datetime, timezone
from pm_predict.domain.money import D, ZERO, dec, fee, floor_tick
from pm_predict.domain.models import Window, Order, Fill, SIDES, TERMINAL
import pm_predict.domain.queries as domain_queries
def budget(self, w, extra):
    day = datetime.fromtimestamp(self.now / 1000, timezone.utc).date().isoformat()
    if self.halted or self.now < self.pause_until:
        return 'account paused'
    if extra > self.cash - domain_queries.reserve(self):
        return 'cash reserved/unavailable'
    if not domain_queries.occupied(self, w) and sum((domain_queries.occupied(self, v) for v in self.windows.values())) >= 2:
        return 'two unsettled windows'
    if max(ZERO, -self.realized) + domain_queries.risk(self) + extra > 20:
        return '20 USD cumulative risk budget'
    if max(ZERO, -self.daily.get(day, ZERO)) + domain_queries.risk(self) + extra > 6:
        return '6 USD daily risk budget'
    return None
