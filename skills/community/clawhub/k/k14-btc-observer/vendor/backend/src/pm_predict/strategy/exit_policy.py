"""Versioned exit pricing hypotheses; pure computation, no market fitting or I/O.

Legacy defaults remain explicit. New profiles must be selected for a NEW lot;
checkpoint restoration must not silently replace an existing lot's policy.
"""
from dataclasses import dataclass, asdict

from pm_predict.domain.money import D, dec
from pm_predict.strategy.exit_routes import ceil_tick


@dataclass(frozen=True)
class ExitPolicy:
    max_pair_attempts: int | None = 3
    retry_ms: int = 300
    receipt_timeout_ms: int = 2000
    profile: str = 'legacy-v1'

    def __post_init__(self):
        expected = (3, 300, 2000) if self.profile == 'legacy-v1' else (None, 2000, 2000)
        if self.profile not in ('legacy-v1', 'continuous-fixed-v1', 'continuous-decay-v1') or (
                self.max_pair_attempts, self.retry_ms, self.receipt_timeout_ms) != expected:
            raise ValueError('unknown or modified frozen exit profile; declare a new version')

    @classmethod
    def continuous(cls, *, decay=True):
        return cls(None, 2000, 2000, 'continuous-decay-v1' if decay else 'continuous-fixed-v1')

    @property
    def is_continuous(self):
        return self.profile != 'legacy-v1'

    def checkpoint(self):
        return asdict(self)

    @classmethod
    def restore(cls, state):
        if set(state) != {'max_pair_attempts', 'retry_ms', 'receipt_timeout_ms', 'profile'}:
            raise ValueError('incomplete exit profile checkpoint')
        return cls(**state)

    def routes(self):
        return dict(max_shares='5', buy_cap='0.50', pair_cap='0.95',
                    merge_allowance_per_share='0.00001', no_buy_age_seconds=840,
                    window_seconds=900)

    def target(self, age_ms):
        if not self.is_continuous:
            return D('0')
        if self.profile == 'continuous-fixed-v1':
            return D('.12')
        return (D('.12'), D('.09'), D('.06'), D('.03'), D('.01'))[
            min(4, max(0, int(age_ms) // 180000))]

    def price_routes(self, routes, snapshot, side, quantity, basis, age_ms):
        """Apply an additional target, never remove an original financial gate.

        Basis includes confirmed entry fees. Maker exit fee remains the verified
        zero-maker schedule; FOK net limits include the existing taker estimate.
        These are decision bounds, not a guarantee about eventual actual fees.
        """
        if not self.is_continuous:
            return routes
        target = self.target(age_ms)
        q, basis = dec(quantity), dec(basis)
        for name in ('sell', 'pair'):
            route = routes[name]
            if route['net_at_limit'] is not None and route['net_at_limit'] < q * target:
                route['eligible'] = False
                route['reasons'].append('below frozen current-stage net-profit target')
        tick = dec(snapshot['market']['tick'])
        best_bid = max(dec(p) for p, _ in snapshot['books'][side]['bids'])
        proposal = ceil_tick(max(basis + target, best_bid + tick), tick)
        # Original quantity/tick/window checks must also allow a Maker order.
        if routes['sell']['maker_ask_proposal'] is not None:
            routes['sell']['maker_ask_proposal'] = proposal if proposal < 1 else None
        sell, pair = routes['sell'], routes['pair']
        routes['recommendation'] = ('SELL' if sell['eligible'] and
            (not pair['eligible'] or sell['net_at_limit'] >= pair['net_at_limit'])
            else 'PAIR' if pair['eligible'] else 'WAIT')
        routes['profit_target_per_share'] = str(target)
        return routes
