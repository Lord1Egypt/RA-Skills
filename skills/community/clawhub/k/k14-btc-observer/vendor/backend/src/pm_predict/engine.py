"""Public engine façade. Services use a single-writer domain state; no web/disk imports."""
from .domain.state import EngineState
from .domain.money import D, fee
import pm_predict.domain.queries as domain_queries
import pm_predict.domain.invariants as domain_invariants
import pm_predict.domain.snapshot as domain_snapshot
import pm_predict.risk.policy as risk_policy
import pm_predict.execution.orders as execution_orders
import pm_predict.market_data.store as market_data_store
import pm_predict.ledger.accounting as ledger_accounting
import pm_predict.coordinator as coordinator

class PaperEngine:
    def __init__(self):
        self.state = EngineState()

    def __getattr__(self, name):
        return getattr(self.state, name)

    def reserve(self, *args, **kwargs):
        return domain_queries.reserve(self.state, *args, **kwargs)

    def risk(self, *args, **kwargs):
        return domain_queries.risk(self.state, *args, **kwargs)

    def check(self, *args, **kwargs):
        return domain_invariants.check(self.state, *args, **kwargs)

    def summary(self, *args, **kwargs):
        return domain_snapshot.summary(self.state, *args, **kwargs)

    def ack(self, *args, **kwargs):
        return execution_orders.ack(self.state, *args, **kwargs)

    def cancel_ack(self, *args, **kwargs):
        return execution_orders.cancel_ack(self.state, *args, **kwargs)

    def reconcile(self, *args, **kwargs):
        return execution_orders.reconcile(self.state, *args, **kwargs)

    def fill(self, *args, **kwargs):
        return execution_orders.fill(self.state, *args, **kwargs)

    def book(self, *args, **kwargs):
        return market_data_store.book(self.state, *args, **kwargs)

    def price(self, *args, **kwargs):
        return market_data_store.price(self.state, *args, **kwargs)

    def health(self, *args, **kwargs):
        return market_data_store.health(self.state, *args, **kwargs)

    def confirm(self, *args, **kwargs):
        return ledger_accounting.confirm(self.state, *args, **kwargs)

    def settle(self, *args, **kwargs):
        return ledger_accounting.settle(self.state, *args, **kwargs)

    def chain_result(self, *args, **kwargs):
        return ledger_accounting.chain_result(self.state, *args, **kwargs)

    def open_window(self, *args, **kwargs):
        return coordinator.open_window(self.state, *args, **kwargs)

    def step(self, *args, **kwargs):
        return coordinator.step(self.state, *args, **kwargs)
