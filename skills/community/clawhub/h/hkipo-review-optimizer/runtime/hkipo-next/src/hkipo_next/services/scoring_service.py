"""Rule-based scoring utilities for compare and future score commands."""

from __future__ import annotations

from typing import Protocol

from hkipo_next.contracts.preferences import ProfileView
from hkipo_next.contracts.scoring import (
    FactorDelta,
    ParameterComparisonData,
    ParameterVersion,
    ScoreCostBreakdown,
    ScoreFactor,
    ScoreSummary,
)
from hkipo_next.contracts.snapshot import SnapshotData


class SnapshotProvider(Protocol):
    """Contract for fetching standardized snapshots by symbol."""

    def snapshot(self, *, symbol: str) -> SnapshotData:
        ...


class ScoringService:
    """Produce stable score summaries from snapshots and parameter versions."""

    def __init__(self, snapshot_provider: SnapshotProvider):
        self.snapshot_provider = snapshot_provider

    def score_symbol(
        self,
        *,
        symbol: str,
        parameter_version: ParameterVersion,
        profile: ProfileView,
    ) -> ScoreSummary:
        snapshot = self.snapshot_provider.snapshot(symbol=symbol)
        return self.score_snapshot(snapshot=snapshot, parameter_version=parameter_version, profile=profile)

    def score_snapshot(
        self,
        *,
        snapshot: SnapshotData,
        parameter_version: ParameterVersion,
        profile: ProfileView,
    ) -> ScoreSummary:
        weights = parameter_version.weights.model_dump()
        total_weight = sum(weights.values())

        quality_score, quality_reason = self._score_quality(snapshot)
        affordability_score, affordability_reason = self._score_affordability(snapshot, profile)
        pricing_score, pricing_reason = self._score_pricing(snapshot)
        sponsor_score, sponsor_reason = self._score_sponsors(snapshot)
        cost_breakdown = self._calculate_costs(snapshot, parameter_version, profile)
        cost_score, cost_reason = self._score_cost_efficiency(cost_breakdown)

        factor_inputs = [
            ("snapshot_quality", quality_score, quality_reason),
            ("affordability", affordability_score, affordability_reason),
            ("pricing_stability", pricing_score, pricing_reason),
            ("sponsor_support", sponsor_score, sponsor_reason),
            ("cost_efficiency", cost_score, cost_reason),
        ]
        factors = [
            ScoreFactor(
                name=name,
                raw_score=round(raw_score, 2),
                weight=round(weights[name] / total_weight, 4),
                contribution=round(raw_score * (weights[name] / total_weight), 2),
                reason=reason,
            )
            for name, raw_score, reason in factor_inputs
        ]
        score = round(sum(factor.contribution for factor in factors), 2)
        action = self._determine_action(score, parameter_version, profile)
        notes = [
            f"parameter_version={parameter_version.parameter_version}",
            f"risk_profile={profile.risk_profile}",
        ]
        if snapshot.quality is not None:
            notes.append(f"snapshot_confidence={snapshot.quality.overall_confidence:.2f}")
        assumptions = [
            f"使用参数版本 {parameter_version.parameter_version}。",
            f"风险偏好为 {profile.risk_profile}，预算上限 {profile.max_budget_hkd:,.2f} HKD。",
            "当前评分基于 standardized snapshot 与规则型因子，不含盘中灰市/新闻实时波动。",
        ]
        if snapshot.deadline_date is not None:
            assumptions.append(f"招股截止日参考 {snapshot.deadline_date.isoformat()}。")
        risk_disclosure = (
            "本结果仅供研究和风险讨论，不构成投资建议；请结合招股书、资金安排、"
            "流动性与市场波动独立判断。"
        )

        return ScoreSummary(
            symbol=snapshot.symbol,
            parameter_version=parameter_version.parameter_version,
            parameter_name=parameter_version.name,
            risk_profile=profile.risk_profile,
            score=score,
            action=action,
            factors=factors,
            cost_breakdown=cost_breakdown,
            assumptions=assumptions,
            risk_disclosure=risk_disclosure,
            source_issue_count=len(snapshot.issues),
            snapshot_overall_confidence=(
                snapshot.quality.overall_confidence if snapshot.quality is not None else None
            ),
            notes=notes,
        )

    def compare_symbol(
        self,
        *,
        symbol: str,
        baseline_version: ParameterVersion,
        candidate_version: ParameterVersion,
        profile: ProfileView,
        active_version: str | None,
        storage_path: str,
    ) -> ParameterComparisonData:
        snapshot = self.snapshot_provider.snapshot(symbol=symbol)
        baseline = self.score_snapshot(
            snapshot=snapshot,
            parameter_version=baseline_version,
            profile=profile,
        )
        candidate = self.score_snapshot(
            snapshot=snapshot,
            parameter_version=candidate_version,
            profile=profile,
        )

        baseline_map = {factor.name: factor.contribution for factor in baseline.factors}
        candidate_map = {factor.name: factor.contribution for factor in candidate.factors}
        factor_deltas = [
            FactorDelta(
                name=name,
                baseline=round(baseline_map.get(name, 0.0), 2),
                candidate=round(candidate_map.get(name, 0.0), 2),
                delta=round(candidate_map.get(name, 0.0) - baseline_map.get(name, 0.0), 2),
            )
            for name in sorted(set(baseline_map) | set(candidate_map))
        ]

        return ParameterComparisonData(
            symbol=baseline.symbol,
            baseline_version=baseline.parameter_version,
            candidate_version=candidate.parameter_version,
            baseline_score=baseline.score,
            candidate_score=candidate.score,
            score_delta=round(candidate.score - baseline.score, 2),
            baseline_action=baseline.action,
            candidate_action=candidate.action,
            action_changed=baseline.action != candidate.action,
            factor_deltas=factor_deltas,
            active_version=active_version,
            risk_profile=profile.risk_profile,
            storage_path=storage_path,
        )

    @staticmethod
    def _score_quality(snapshot: SnapshotData) -> tuple[float, str]:
        if snapshot.quality is None:
            return 55.0, "缺少显式质量层，按中性质量分处理。"
        return (
            round(snapshot.quality.overall_confidence * 100, 2),
            f"整体置信度 {snapshot.quality.overall_confidence:.2f}。",
        )

    @staticmethod
    def _score_affordability(snapshot: SnapshotData, profile: ProfileView) -> tuple[float, str]:
        if snapshot.entry_fee_hkd is None:
            return 50.0, "缺少入场费，按中性预算压力处理。"
        ratio = snapshot.entry_fee_hkd / profile.max_budget_hkd
        if ratio <= 0.25:
            score = 90.0
        elif ratio <= 0.5:
            score = 80.0
        elif ratio <= 0.75:
            score = 70.0
        elif ratio <= 1.0:
            score = 60.0
        elif ratio <= 1.25:
            score = 45.0
        else:
            score = 30.0
        return score, f"入场费占预算比例 {ratio:.2f}。"

    @staticmethod
    def _score_pricing(snapshot: SnapshotData) -> tuple[float, str]:
        floor = snapshot.offer_price_floor
        ceiling = snapshot.offer_price_ceiling
        if floor is None or ceiling is None or floor <= 0:
            return 45.0, "价格区间不完整，按偏保守稳定性处理。"
        spread_pct = ((ceiling - floor) / floor) * 100
        if spread_pct <= 2:
            score = 90.0
        elif spread_pct <= 5:
            score = 80.0
        elif spread_pct <= 10:
            score = 70.0
        elif spread_pct <= 15:
            score = 55.0
        else:
            score = 40.0
        return score, f"发行区间宽度 {spread_pct:.2f}% 。"

    @staticmethod
    def _score_sponsors(snapshot: SnapshotData) -> tuple[float, str]:
        sponsor_count = len(snapshot.sponsors)
        if sponsor_count >= 2:
            score = 82.0
        elif sponsor_count == 1:
            score = 68.0
        else:
            score = 45.0
        return score, f"保荐人数量 {sponsor_count}。"

    @staticmethod
    def _calculate_costs(
        snapshot: SnapshotData,
        parameter_version: ParameterVersion,
        profile: ProfileView,
    ) -> ScoreCostBreakdown:
        entry_fee = snapshot.entry_fee_hkd or 0.0
        costs = parameter_version.costs
        financing_base = 0.0
        if profile.financing_preference == "margin":
            financing_base = entry_fee
        elif profile.financing_preference == "auto" and entry_fee > profile.max_budget_hkd:
            financing_base = max(entry_fee - profile.max_budget_hkd, 0.0)

        financing_cost = financing_base * (costs.financing_rate_annual_pct / 100) * (costs.lockup_days / 365)
        opportunity_base = min(entry_fee, profile.max_budget_hkd) if entry_fee else 0.0
        opportunity_cost = (
            opportunity_base
            * (costs.cash_opportunity_rate_annual_pct / 100)
            * (costs.lockup_days / 365)
        )
        total_cost = costs.handling_fee_hkd + financing_cost + opportunity_cost
        cost_ratio_pct = (total_cost / entry_fee * 100) if entry_fee > 0 else 0.0
        return ScoreCostBreakdown(
            handling_fee_hkd=round(costs.handling_fee_hkd, 2),
            financing_cost_hkd=round(financing_cost, 2),
            opportunity_cost_hkd=round(opportunity_cost, 2),
            total_cost_hkd=round(total_cost, 2),
            cost_ratio_pct=round(cost_ratio_pct, 2),
        )

    @staticmethod
    def _score_cost_efficiency(cost_breakdown: ScoreCostBreakdown) -> tuple[float, str]:
        ratio = cost_breakdown.cost_ratio_pct
        if ratio <= 0.5:
            score = 90.0
        elif ratio <= 1.0:
            score = 80.0
        elif ratio <= 2.0:
            score = 65.0
        elif ratio <= 3.0:
            score = 50.0
        else:
            score = 35.0
        return score, f"总成本占入场费比例 {ratio:.2f}% 。"

    @staticmethod
    def _determine_action(
        score: float,
        parameter_version: ParameterVersion,
        profile: ProfileView,
    ) -> str:
        profile_modifier = {
            "conservative": 5.0,
            "balanced": 0.0,
            "aggressive": -5.0,
        }[profile.risk_profile]
        participate_min = min(max(parameter_version.thresholds.participate_min + profile_modifier, 0.0), 100.0)
        cautious_min = min(
            max(parameter_version.thresholds.cautious_min + (profile_modifier / 2), 0.0),
            participate_min - 0.01,
        )
        if score >= participate_min:
            return "participate"
        if score >= cautious_min:
            return "cautious"
        return "pass"
