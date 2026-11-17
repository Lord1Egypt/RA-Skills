"""Mechanically extracted from the verified paper prototype; single-writer EngineState."""
from datetime import datetime, timezone
from pm_predict.domain.money import D, ZERO, dec, fee, floor_tick
from pm_predict.domain.models import Window, Order, Fill, SIDES, TERMINAL
import pm_predict.domain.invariants as domain_invariants
import pm_predict.domain.queries as domain_queries
import pm_predict.execution.orders as execution_orders
import pm_predict.ledger.accounting as ledger_accounting
import pm_predict.market_data.store as market_data_store
from pm_predict.strategy.indicators import Bar, fair_up, k14, signal
def open_window(self, market, start, bars, thresholds, ptb, tick='0.01', min_qty='5', rule_verified=False, ptb_source='UNKNOWN', fee_rate='0.07', now=None):
    now = start * 1000 if now is None else now
    if now < start * 1000:
        raise ValueError('cannot lock a closing-bar signal before the window starts')
    self._time(now)
    if market in self.windows or start % 900:
        raise ValueError('duplicate/non-M15 market')
    if not rule_verified or ptb_source != 'CHAINLINK_TWAP60_AT_START' or dec(fee_rate) != D('0.07'):
        self._log('SKIP_MARKET', market=market, reason='rules/official start price unknown or changed')
        return
    tick, min_qty = (dec(tick), dec(min_qty))
    if tick not in map(D, ('0.1', '0.01', '0.005', '0.0025', '0.001', '0.0001')) or min_qty <= 0:
        raise ValueError('invalid market increments')
    if dec(ptb) <= 0:
        raise ValueError('invalid start price')
    rows = [Bar(**r) if isinstance(r, dict) else r for r in bars]
    k = k14(rows, start)
    side = signal(k, thresholds, start)
    self.windows[market] = Window(market, start, side, k, bool(thresholds.get('provisional', True)), tick, min_qty, float(ptb))
    self._log('SIGNAL', market=market, k14=k, side=side, provisional=self.windows[market].provisional)

def step(self, market, now):
    self._time(now)
    w = self.windows[market]
    age = now / 1000 - w.start
    for o in domain_queries.active(self, market):
        waiting_since = o.cancel_ms if o.status == 'CANCEL_PENDING' else o.sent_ms
        if o.status in ('SENT', 'CANCEL_PENDING') and now - waiting_since > 2000:
            execution_orders.block(self, w, 'order receipt timed out; reserve retained')
    if age >= 120:
        execution_orders.cancel(self, w, 'entry deadline')
    if self.halted or self.now < self.pause_until:
        execution_orders.cancel(self, w, 'account paused')
        return
    if not domain_queries.pending(self, market) and w.winner is None:
        ledger_accounting.merge(self, w)
    if w.blocked or self.halted or (not 0 <= age < 840) or w.closed:
        return
    if not market_data_store.fresh(self, w):
        execution_orders.block(self, w, 'feed/clock/trader lease unhealthy')
        return
    w.fair = fair_up(w.spot, w.ptb, w.sigma, 900 - age)
    if w.fair is None:
        execution_orders.block(self, w, 'invalid/zero volatility')
        return
    if not w.side:
        return
    f = dec(w.fair if w.side == 'Up' else 1 - w.fair)
    own = w.books[w.side]
    p = floor_tick(min(own[2] + w.tick, D('0.48'), f + D('0.02'), own[3][0][0] - w.tick), w.tick)
    active = domain_queries.active(self, market, 'ENTRY')
    if active:
        for o in active:
            if o.price > f + D('0.02'):
                execution_orders.cancel(self, w, 'fair value moved adversely')
            elif o.status == 'LIVE' and own[2] > o.price and (p > o.price) and (now - w.last_quote_ms >= 300) and (w.quote_count < 7):
                execution_orders.cancel(self, w, 'outbid; replace only after terminal reconciliation')
    elif age < 120 and w.quote_count < 7 and (now - w.last_quote_ms >= 300):
        used = sum((domain_queries.filled(self, o.id) for o in self.orders.values() if o.market == market and o.kind == 'ENTRY'), ZERO)
        remaining = D('5') - used
        if p >= D('0.30') and remaining >= w.min_qty:
            if execution_orders.send(self, w, w.side, remaining, p, 'ENTRY'):
                w.quote_count += 1
                w.last_quote_ms = now
    hedge(self, w)
    ledger_accounting.merge(self, w)
    domain_invariants.check(self)

def hedge(self, w):
    if w.hedge_attempted or w.maintenance or w.chain or domain_queries.pending(self, w.id):
        return
    other = 'Down' if w.side == 'Up' else 'Up'
    qty = w.qty[w.side] - w.qty[other]
    if qty < w.min_qty or qty % D('0.01'):
        return
    left, cost, worst = (qty, ZERO, ZERO)
    for price, size in w.books[other][3]:
        if price > D('0.50'):
            break
        take = min(left, size)
        cost += take * price + fee(take, price)
        worst = price
        left -= take
        if not left:
            break
    if left:
        self._log('HEDGE_UNAVAILABLE', market=w.id, reason='depth/0.50 cap')
        return
    basis = w.cost[w.side] / w.qty[w.side]
    bound = qty * worst + fee(qty, worst) + D('0.00001') * qty
    if basis * qty + bound > D('0.95') * qty:
        self._log('HEDGE_UNAVAILABLE', market=w.id, reason='worst-case all-in cost > 0.95')
        return
    if execution_orders.send(self, w, other, qty, worst, 'HEDGE'):
        w.hedge_attempted = True
        self._log('HEDGE_DEPTH', market=w.id, snapshot_cost=str(cost), reserved_bound=str(bound))
