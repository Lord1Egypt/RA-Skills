"""Decision-card generation on top of scoring output."""

from __future__ import annotations

from typing import Protocol

from hkipo_next.contracts.decision_card import DecisionCardData, ExitPlan, PositionSuggestion
from hkipo_next.contracts.preferences import ProfileView
from hkipo_next.contracts.scoring import ParameterVersion, ScoreSummary


class ScoreProvider(Protocol):
    """Contract for producing score summaries."""

    def score_symbol(
        self,
        *,
        symbol: str,
        parameter_version: ParameterVersion,
        profile: ProfileView,
    ) -> ScoreSummary:
        ...


class DecisionService:
    """Generate action-oriented decision cards from score summaries."""

    def __init__(self, score_provider: ScoreProvider):
        self.score_provider = score_provider

    def build_for_symbol(
        self,
        *,
        symbol: str,
        parameter_version: ParameterVersion,
        profile: ProfileView,
    ) -> DecisionCardData:
        summary = self.score_provider.score_symbol(
            symbol=symbol,
            parameter_version=parameter_version,
            profile=profile,
        )
        return self.build_from_score(summary=summary, profile=profile)

    def build_from_score(self, *, summary: ScoreSummary, profile: ProfileView) -> DecisionCardData:
        position = self._build_position(summary=summary, profile=profile)
        exit_plan = self._build_exit_plan(summary=summary, profile=profile)
        sorted_factors = sorted(summary.factors, key=lambda factor: factor.contribution, reverse=True)
        top_reasons = [f"{factor.name}: {factor.reason}" for factor in sorted_factors[:3]]
        headline_map = {
            "participate": "可以按纪律参与，但要严格遵守仓位和退出阈值。",
            "cautious": "存在参与空间，但更适合轻仓或继续观察。",
            "pass": "当前性价比不足，建议放弃并保留观察。",
        }
        return DecisionCardData(
            symbol=summary.symbol,
            decision=summary.action,
            headline=headline_map[summary.action],
            score=summary.score,
            parameter_version=summary.parameter_version,
            risk_profile=summary.risk_profile,
            position_suggestion=position,
            exit_plan=exit_plan,
            top_reasons=top_reasons,
            risk_disclosure=summary.risk_disclosure,
            cost_breakdown=summary.cost_breakdown,
            source_issue_count=summary.source_issue_count,
        )

    @staticmethod
    def _build_position(*, summary: ScoreSummary, profile: ProfileView) -> PositionSuggestion:
        base_pct = {
            "conservative": 25.0,
            "balanced": 50.0,
            "aggressive": 75.0,
        }[profile.risk_profile]
        action_multiplier = {
            "participate": 1.0,
            "cautious": 0.5,
            "pass": 0.0,
        }[summary.action]
        position_size_pct = round(base_pct * action_multiplier, 2)
        suggested_budget_hkd = round(profile.max_budget_hkd * (position_size_pct / 100), 2)
        if summary.action == "pass":
            subscription_mode = "watch-only"
        elif profile.financing_preference == "margin":
            subscription_mode = "margin"
        elif profile.financing_preference == "auto" and summary.cost_breakdown.cost_ratio_pct <= 1.0:
            subscription_mode = "margin"
        else:
            subscription_mode = "cash"
        return PositionSuggestion(
            position_size_pct=position_size_pct,
            suggested_budget_hkd=suggested_budget_hkd,
            subscription_mode=subscription_mode,
        )

    @staticmethod
    def _build_exit_plan(*, summary: ScoreSummary, profile: ProfileView) -> ExitPlan:
        base_plan = {
            "conservative": (12.0, 5.0, 2),
            "balanced": (18.0, 7.0, 3),
            "aggressive": (25.0, 10.0, 5),
        }[profile.risk_profile]
        take_profit, stop_loss, holding_days = base_plan
        if summary.action == "cautious":
            take_profit -= 3.0
            stop_loss -= 1.5
        if summary.action == "pass":
            return ExitPlan(
                take_profit_pct=0.0,
                stop_loss_pct=0.0,
                max_holding_days=0,
                note="当前建议为放弃，不进入执行与退出流程。",
            )
        note = "达到止盈/止损阈值或超过计划持有天数时，按纪律退出。"
        if summary.source_issue_count:
            note += " 由于存在数据缺口，请在执行前再做一次人工复核。"
        return ExitPlan(
            take_profit_pct=round(take_profit, 2),
            stop_loss_pct=round(stop_loss, 2),
            max_holding_days=holding_days,
            note=note,
        )
