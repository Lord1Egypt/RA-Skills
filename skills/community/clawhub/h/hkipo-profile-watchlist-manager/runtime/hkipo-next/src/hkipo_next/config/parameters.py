"""Parameter version repository and builders."""

from __future__ import annotations

from argparse import Namespace

from hkipo_next.contracts.scoring import CostModel, DecisionThresholds, FactorWeights, ParameterSet, ParameterVersion
from hkipo_next.storage.sqlite_store import SQLiteStore


class ParameterRepository:
    """High-level repository for scoring parameter versions."""

    def __init__(self, store: SQLiteStore):
        self.store = store
        self.store.initialize()

    def save(self, parameter_set: ParameterSet, *, activate: bool | None = None) -> ParameterVersion:
        if activate is None:
            activate = self.get_active() is None
        return self.store.save_parameter_set(parameter_set, activate=activate)

    def list(self) -> list[ParameterVersion]:
        return self.store.list_parameter_sets()

    def get(self, version_id: str) -> ParameterVersion | None:
        return self.store.get_parameter_set(version_id)

    def get_active(self) -> ParameterVersion | None:
        return self.store.get_active_parameter_set()

    def use(self, version_id: str) -> ParameterVersion:
        return self.store.set_active_parameter_set(version_id)

    @property
    def storage_path(self) -> str:
        return str(self.store.path)


def build_parameter_set_from_args(args: Namespace) -> ParameterSet:
    default_weights = FactorWeights()
    default_thresholds = DecisionThresholds()
    default_costs = CostModel()
    return ParameterSet(
        name=args.name,
        weights=FactorWeights(
            snapshot_quality=_coalesce(args.snapshot_quality_weight, default_weights.snapshot_quality),
            affordability=_coalesce(args.affordability_weight, default_weights.affordability),
            pricing_stability=_coalesce(
                args.pricing_stability_weight,
                default_weights.pricing_stability,
            ),
            sponsor_support=_coalesce(args.sponsor_support_weight, default_weights.sponsor_support),
            cost_efficiency=_coalesce(args.cost_efficiency_weight, default_weights.cost_efficiency),
        ),
        thresholds=DecisionThresholds(
            participate_min=_coalesce(args.participate_min, default_thresholds.participate_min),
            cautious_min=_coalesce(args.cautious_min, default_thresholds.cautious_min),
        ),
        costs=CostModel(
            handling_fee_hkd=_coalesce(args.handling_fee_hkd, default_costs.handling_fee_hkd),
            financing_rate_annual_pct=_coalesce(
                args.financing_rate_annual_pct,
                default_costs.financing_rate_annual_pct,
            ),
            cash_opportunity_rate_annual_pct=(
                _coalesce(
                    args.cash_opportunity_rate_annual_pct,
                    default_costs.cash_opportunity_rate_annual_pct,
                )
            ),
            lockup_days=_coalesce(args.lockup_days, default_costs.lockup_days),
        ),
        notes=args.notes,
    )


def _coalesce(value, default):
    return default if value is None else value
