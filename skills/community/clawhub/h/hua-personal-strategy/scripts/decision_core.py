"""Pure deterministic allocation, factor-risk, amount, and invariant logic for v4.3.0."""

from __future__ import annotations

import hashlib
import json
import math
from copy import deepcopy
from datetime import date
from decimal import Decimal, ROUND_DOWN
from pathlib import Path
from typing import Any

try:
    from .policy_store import next_question, validate_policy
except ImportError:
    from policy_store import next_question, validate_policy


STRATEGY_VERSION = "4.3.0"
ENGINE_VERSION = "4.3.0"
CONTEXT_SCHEMA = "quant_strategy_context.v2"
AI_SCHEMA = "ai_investment_view.v1"
DECISION_SCHEMA = "decision_result.v1"
ACTIVITY_SCHEMA_V2 = "portfolio_activity.v2"
ORDINARY_BUY_ACTIONS = {"CONTRIBUTION_REBALANCE", "TACTICAL_ROTATE"}
BUY_ACTIONS = ORDINARY_BUY_ACTIONS | {"REENTRY_AFTER_RISK_OFF"}
SELL_ACTIONS = {"STRATEGIC_REBALANCE", "RISK_REDUCE", "TACTICAL_ROTATE"}
BLOCKED_PURCHASE_WORDS = ("暂停", "关闭", "不可", "终止")
BLOCKED_REDEMPTION_WORDS = ("暂停", "关闭", "不可", "终止")
TREND_FACTOR_METHOD = "fund_trend_consensus_v1"
TREND_FACTOR_FIELDS = ("r20", "r60", "priceVsMa20", "ma20VsMa60")
FACTOR_COVERAGE_MIN_PCT = 80.0
FACTOR_CONSENSUS_MIN_PCT = 60.0
DRAWDOWN_SCOPE_MCP = "MCP_FUND_PORTFOLIO"
DRAWDOWN_SCOPE_TOTAL = "TOTAL_INVESTABLE_ASSETS"
DRAWDOWN_METHOD_MCP = "MCP_REPORTED"
DRAWDOWN_METHOD_TOTAL_PROXY = "STATIC_CASH_PROXY_V1"


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), default=str)


def object_hash(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def load_ai_governance() -> dict[str, Any]:
    path = Path(__file__).resolve().parents[1] / "references" / "ai-output-governance.json"
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict) or value.get("schemaVersion") != "ai_output_governance.v1":
        raise ValueError("invalid ai output governance")
    return value


def number(value: Any, default: float = 0.0) -> float:
    if isinstance(value, bool):
        return default
    try:
        parsed = float(value)
    except (TypeError, ValueError):
        return default
    return parsed if math.isfinite(parsed) else default


def clamp(value: float, low: float, high: float) -> float:
    return min(high, max(low, value))


def floor_step(value: float, step: float) -> float:
    if value <= 0 or step <= 0:
        return 0.0
    quantized = (Decimal(str(value)) / Decimal(str(step))).to_integral_value(rounding=ROUND_DOWN)
    return float(quantized * Decimal(str(step)))


def base_result(status: str, action: str, blockers: list[str] | None = None) -> dict[str, Any]:
    return {
        "schemaVersion": DECISION_SCHEMA,
        "status": status,
        "executionMode": "NONE",
        "action": action,
        "scope": None,
        "fundCode": None,
        "fundName": None,
        "amountCny": None,
        "currentWeightPct": None,
        "targetWeightPct": None,
        "targetBandPct": [None, None],
        "changeWeightPct": None,
        "drivers": [],
        "blockers": list(dict.fromkeys(blockers or [])),
        "confidence": "NONE",
        "validUntil": None,
        "nextReviewAt": None,
        "dataAsOf": None,
        "amountTrace": {},
        "invalidationTriggers": [],
        "allocation": {},
        "audit": {
            "strategyVersion": STRATEGY_VERSION,
            "engineVersion": ENGINE_VERSION,
        },
    }


def finish(result: dict[str, Any], payload: dict[str, Any]) -> dict[str, Any]:
    audit = result.setdefault("audit", {})
    audit["canonicalInputHash"] = object_hash(payload)
    without_output_hash = deepcopy(result)
    without_output_hash.setdefault("audit", {}).pop("canonicalOutputHash", None)
    audit["canonicalOutputHash"] = object_hash(without_output_hash)
    return result


def needs_profile(policy: dict[str, Any] | None, payload: dict[str, Any]) -> dict[str, Any]:
    result = base_result("NEEDS_PROFILE", "NEEDS_PROFILE", ["INVESTOR_POLICY_NOT_ACTIVE"])
    result["nextQuestion"] = next_question(policy)
    if policy:
        result["audit"]["policyVersion"] = policy.get("policyVersion")
    return finish(result, payload)


def validate_ai_view(ai_view: dict[str, Any], policy: dict[str, Any], context: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if not isinstance(ai_view, dict):
        return ["AI_VIEW_MISSING"]
    if ai_view.get("schemaVersion") != AI_SCHEMA:
        errors.append("AI_VIEW_SCHEMA_INVALID")
    if ai_view.get("status") != "VALID":
        errors.append("AI_VIEW_NOT_VALID")
    if ai_view.get("asOfDate") != context.get("asOfDate"):
        errors.append("AI_VIEW_AS_OF_MISMATCH")
    model_version = str(ai_view.get("modelVersion") or "").strip()
    if not model_version:
        errors.append("AI_MODEL_VERSION_MISSING")
    if not str(ai_view.get("promptVersion") or "").strip():
        errors.append("AI_PROMPT_VERSION_MISSING")
    if not str(ai_view.get("evidenceSetHash") or "").strip():
        errors.append("AI_EVIDENCE_HASH_MISSING")
    attestation = ai_view.get("capabilityAttestation") if isinstance(ai_view.get("capabilityAttestation"), dict) else {}
    governance = load_ai_governance()
    if governance.get("requireEvidenceGrounded") and attestation.get("evidenceGrounded") is not True:
        errors.append("AI_NOT_EVIDENCE_GROUNDED")
    if governance.get("requireIndependentCritic") and attestation.get("criticIndependent") is not True:
        errors.append("AI_CRITIC_NOT_INDEPENDENT")
    if attestation.get("numericAuthority") != governance.get("numericAuthority"):
        errors.append("AI_NUMERIC_AUTHORITY_FORBIDDEN")
    if ai_view.get("criticVerdict") not in {"PASS", "PASS_WITH_LIMITS"}:
        errors.append("AI_CRITIC_BLOCKED")

    probabilities = ai_view.get("scenarioProbabilities")
    if not isinstance(probabilities, dict) or abs(sum(number(v) for v in probabilities.values()) - 1.0) > 0.001:
        errors.append("AI_SCENARIO_PROBABILITIES_INVALID")
    known_sleeves = {str(item.get("id")) for item in policy.get("assetSleeves") or [] if isinstance(item, dict)}
    evidence_ids: set[str] = set()
    for index, item in enumerate(ai_view.get("evidence") or []):
        if not isinstance(item, dict) or not item.get("id"):
            errors.append(f"AI_EVIDENCE_{index}_INVALID")
            continue
        evidence_id = str(item["id"])
        if evidence_id in evidence_ids:
            errors.append(f"AI_EVIDENCE_{index}_DUPLICATE")
        evidence_ids.add(evidence_id)
        if not str(item.get("source") or "").strip() or not str(item.get("fact") or "").strip():
            errors.append(f"AI_EVIDENCE_{index}_SOURCE_OR_FACT_MISSING")
        evidence_as_of = str(item.get("asOfDate") or "")
        if evidence_as_of and evidence_as_of > str(context.get("asOfDate") or ""):
            errors.append(f"AI_EVIDENCE_{index}_FROM_FUTURE")
    seen_sleeves: set[str] = set()
    for index, view in enumerate(ai_view.get("sleeveViews") or []):
        if not isinstance(view, dict):
            errors.append(f"AI_SLEEVE_VIEW_{index}_INVALID")
            continue
        sleeve_id = str(view.get("sleeveId") or "")
        if sleeve_id not in known_sleeves or sleeve_id in seen_sleeves:
            errors.append(f"AI_SLEEVE_VIEW_{index}_UNKNOWN_OR_DUPLICATE")
        seen_sleeves.add(sleeve_id)
        direction = str(view.get("direction") or "")
        if direction not in {"OVERWEIGHT", "NEUTRAL", "UNDERWEIGHT", "EXIT_REVIEW"}:
            errors.append(f"AI_SLEEVE_VIEW_{index}_DIRECTION_INVALID")
        confidence = number(view.get("confidence"), -1)
        if not 0 <= confidence <= 1:
            errors.append(f"AI_SLEEVE_VIEW_{index}_CONFIDENCE_INVALID")
        delta = number(view.get("proposedDeltaPct"))
        if direction == "OVERWEIGHT" and delta < 0:
            errors.append(f"AI_SLEEVE_VIEW_{index}_DELTA_SIGN_INVALID")
        if direction in {"UNDERWEIGHT", "EXIT_REVIEW"} and delta > 0:
            errors.append(f"AI_SLEEVE_VIEW_{index}_DELTA_SIGN_INVALID")
        referenced = [str(item) for item in view.get("evidenceIds") or []]
        counter = [str(item) for item in view.get("counterEvidenceIds") or []]
        if direction != "NEUTRAL" and not referenced:
            errors.append(f"AI_SLEEVE_VIEW_{index}_EVIDENCE_REQUIRED")
        if any(item not in evidence_ids for item in [*referenced, *counter]):
            errors.append(f"AI_SLEEVE_VIEW_{index}_EVIDENCE_UNKNOWN")
        if direction != "NEUTRAL" and not view.get("invalidationTriggers"):
            errors.append(f"AI_SLEEVE_VIEW_{index}_INVALIDATION_REQUIRED")
    return list(dict.fromkeys(errors))


def index_policy(policy: dict[str, Any]) -> tuple[dict[str, dict[str, Any]], str]:
    sleeves = {
        str(item["id"]): item
        for item in policy.get("assetSleeves") or []
        if isinstance(item, dict) and item.get("id")
    }
    cash_ids = [key for key, item in sleeves.items() if item.get("assetClass") == "CASH"]
    return sleeves, cash_ids[0]


def ai_view_by_sleeve(ai_view: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {
        str(item.get("sleeveId")): item
        for item in ai_view.get("sleeveViews") or []
        if isinstance(item, dict) and item.get("sleeveId")
    }


def sleeve_matches_portfolio_limit(sleeve: dict[str, Any], limit_field: str) -> bool:
    asset_class = str(sleeve.get("assetClass") or "")
    if limit_field == "maxEquityWeightPct":
        return asset_class.startswith("EQUITY") or asset_class.startswith("THEME")
    if limit_field == "maxThemeWeightPct":
        return asset_class.startswith("THEME") or "_THEME" in asset_class
    return False


def _metric_value(metrics: dict[str, Any], field: str) -> float | None:
    raw = metrics.get(field)
    if isinstance(raw, bool) or raw is None:
        return None
    try:
        value = float(raw)
    except (TypeError, ValueError):
        return None
    return value if math.isfinite(value) else None


def sleeve_factor_states(
    policy: dict[str, Any],
    context: dict[str, Any],
    values: dict[str, float],
) -> dict[str, dict[str, Any]]:
    """Derive auditable trend consensus only from MCP fund metrics, never AI prose."""
    sleeves, cash_id = index_policy(policy)
    mapping = {str(code): str(sleeve_id) for code, sleeve_id in (policy.get("fundSleeveMap") or {}).items()}
    holdings = holding_map(context)
    states: dict[str, dict[str, Any]] = {}
    for sleeve_id in sleeves:
        if sleeve_id == cash_id:
            continue
        sleeve_codes = [code for code, mapped in mapping.items() if mapped == sleeve_id and values.get(code, 0) > 0]
        total_value = sum(values.get(code, 0.0) for code in sleeve_codes)
        factor_weights = {
            field: {"covered": 0.0, "adverse": 0.0, "positive": 0.0}
            for field in TREND_FACTOR_FIELDS
        }
        for code in sleeve_codes:
            holding = holdings.get(code) or {}
            metrics = holding.get("metrics") if isinstance(holding.get("metrics"), dict) else {}
            if metrics.get("complete") is not True:
                continue
            weight = max(0.0, values.get(code, 0.0))
            r20 = _metric_value(metrics, "r20Pct")
            r60 = _metric_value(metrics, "r60Pct")
            bias20 = _metric_value(metrics, "bias20Pct")
            ma20 = _metric_value(metrics, "ma20")
            ma60 = _metric_value(metrics, "ma60")
            observations = {
                "r20": None if r20 is None else (r20 < 0, r20 > 0),
                "r60": None if r60 is None else (r60 < 0, r60 > 0),
                "priceVsMa20": None if bias20 is None else (bias20 < 0, bias20 > 0),
                "ma20VsMa60": None if ma20 is None or ma60 is None else (ma20 < ma60, ma20 > ma60),
            }
            for factor, observation in observations.items():
                if observation is None:
                    continue
                factor_weights[factor]["covered"] += weight
                if observation[0]:
                    factor_weights[factor]["adverse"] += weight
                if observation[1]:
                    factor_weights[factor]["positive"] += weight

        factors: dict[str, dict[str, Any]] = {}
        for factor, weights in factor_weights.items():
            coverage_pct = weights["covered"] / total_value * 100 if total_value > 0 else 0.0
            adverse_pct = weights["adverse"] / weights["covered"] * 100 if weights["covered"] > 0 else 0.0
            positive_pct = weights["positive"] / weights["covered"] * 100 if weights["covered"] > 0 else 0.0
            state = "UNKNOWN"
            if coverage_pct >= FACTOR_COVERAGE_MIN_PCT:
                if adverse_pct >= FACTOR_CONSENSUS_MIN_PCT:
                    state = "ADVERSE"
                elif positive_pct >= FACTOR_CONSENSUS_MIN_PCT:
                    state = "POSITIVE"
                else:
                    state = "MIXED"
            factors[factor] = {
                "state": state,
                "coveragePct": round(coverage_pct, 4),
                "adverseWeightPct": round(adverse_pct, 4),
                "positiveWeightPct": round(positive_pct, 4),
            }
        coverage_complete = total_value > 0 and all(
            item["coveragePct"] >= FACTOR_COVERAGE_MIN_PCT for item in factors.values()
        )
        adverse_count = sum(1 for item in factors.values() if item["state"] == "ADVERSE")
        positive_count = sum(1 for item in factors.values() if item["state"] == "POSITIVE")
        severity = "UNKNOWN" if not coverage_complete else (
            "SEVERE" if adverse_count == 4 else
            "STRONG" if adverse_count == 3 else
            "CONFIRMED" if adverse_count == 2 else
            "MIXED"
        )
        states[sleeve_id] = {
            "schemaVersion": "risk_factor_state.v1",
            "method": TREND_FACTOR_METHOD,
            "dataComplete": coverage_complete,
            "investedValueCny": round(total_value, 2),
            "adverseFactorCount": adverse_count,
            "positiveFactorCount": positive_count,
            "severity": severity,
            "factors": factors,
        }
    return states


def soft_risk_adjustment(
    policy: dict[str, Any],
    current_weights: dict[str, float],
    targets: dict[str, float],
    factor_states: dict[str, dict[str, Any]],
) -> tuple[dict[str, float], str | None, float]:
    controls = policy.get("riskControls") if isinstance(policy.get("riskControls"), dict) else {}
    if controls.get("factorMethod") != TREND_FACTOR_METHOD:
        return targets, None, 0.0
    sleeves, cash_id = index_policy(policy)
    minimum_adverse = int(number(controls.get("minimumAdverseFactorCount"), 5))
    candidates = []
    for sleeve_id, sleeve in sleeves.items():
        state = factor_states.get(sleeve_id) or {}
        if sleeve_id == cash_id or number(sleeve.get("riskLevel")) <= 0 or state.get("dataComplete") is not True:
            continue
        adverse_count = int(number(state.get("adverseFactorCount")))
        reducible = current_weights.get(sleeve_id, 0.0) - number(sleeve.get("minWeightPct"))
        if adverse_count >= minimum_adverse and reducible > 0.01:
            candidates.append((adverse_count, current_weights.get(sleeve_id, 0.0), sleeve_id))
    if not candidates:
        return targets, None, 0.0
    adverse_count, _, sleeve_id = max(candidates)
    steps = controls.get("reductionStepPctByAdverseFactorCount") or {}
    requested_step = number(steps.get(str(adverse_count)))
    sleeve_min = number(sleeves[sleeve_id].get("minWeightPct"))
    cash_capacity = max(0.0, number(sleeves[cash_id].get("maxWeightPct")) - targets.get(cash_id, 0.0))
    actual_step = min(
        requested_step,
        max(0.0, current_weights.get(sleeve_id, 0.0) - sleeve_min),
        cash_capacity,
    )
    if actual_step <= 0.01:
        return targets, None, 0.0
    adjusted = dict(targets)
    adjusted[sleeve_id] = max(
        sleeve_min,
        min(adjusted.get(sleeve_id, current_weights.get(sleeve_id, 0.0)), current_weights.get(sleeve_id, 0.0) - actual_step),
    )
    adjusted[cash_id] = 100.0 - sum(value for key, value in adjusted.items() if key != cash_id)
    return adjusted, sleeve_id, current_weights.get(sleeve_id, 0.0) - adjusted[sleeve_id]


def effective_monthly_turnover_limit_pct(
    policy: dict[str, Any],
    action: str,
    side: str,
    factor_state: dict[str, Any],
    view: dict[str, Any],
) -> tuple[float | None, list[str]]:
    hard_cap = number((policy.get("portfolioLimits") or {}).get("maxMonthlyTurnoverPct"))
    controls = policy.get("riskControls") if isinstance(policy.get("riskControls"), dict) else {}
    dynamic = controls.get("dynamicTurnover") if isinstance(controls.get("dynamicTurnover"), dict) else {}
    if dynamic.get("enabled") is not True:
        return hard_cap, ["FIXED_POLICY_TURNOVER_CAP"]
    if action == "RISK_REDUCE" and dynamic.get("riskReductionExempt") is True:
        return None, ["RISK_REDUCTION_EXEMPT_FROM_NORMAL_TURNOVER"]
    if action == "STRATEGIC_REBALANCE":
        return hard_cap, ["POLICY_BAND_REBALANCE_USES_HARD_CAP"]
    if factor_state.get("dataComplete") is not True:
        return 0.0, ["DYNAMIC_TURNOVER_FACTOR_DATA_INCOMPLETE"]
    factor_count = int(number(
        factor_state.get("positiveFactorCount") if side == "BUY" else factor_state.get("adverseFactorCount")
    ))
    tier_step = number(dynamic.get("tierStepPct"))
    minimum_confirming = int(number(dynamic.get("minimumConfirmingFactorCount"), 4))
    factor_cap = 0.0 if factor_count < minimum_confirming else min(hard_cap, factor_count * tier_step)
    confidence = number(view.get("confidence"))
    confidence_tiers = 0 if confidence < 0.55 else 2 if confidence < 0.70 else 3 if confidence < 0.80 else 4
    confidence_cap = min(hard_cap, confidence_tiers * tier_step)
    return min(hard_cap, factor_cap, confidence_cap), [
        "FACTOR_TIERED_TURNOVER",
        f"FACTOR_COUNT_{factor_count}",
        f"CONFIDENCE_TIER_{confidence_tiers}",
    ]


def risk_off_reentry_capacity_pct(
    policy: dict[str, Any],
    context: dict[str, Any],
    activity: dict[str, Any],
    factor_state: dict[str, Any],
    view: dict[str, Any],
) -> tuple[float, list[str]]:
    """Return a separate, conservative re-entry budget after a classified protective sell."""
    controls = policy.get("riskControls") if isinstance(policy.get("riskControls"), dict) else {}
    config = controls.get("riskOffReentry") if isinstance(controls.get("riskOffReentry"), dict) else {}
    if config.get("enabled") is not True:
        return 0.0, ["RISK_OFF_REENTRY_DISABLED"]
    if activity.get("schemaVersion") != ACTIVITY_SCHEMA_V2:
        return 0.0, ["RISK_OFF_REENTRY_REQUIRES_ACTIVITY_V2"]
    protective = number(activity.get("protectiveSellTurnoverPct"))
    reentry_used = number(activity.get("riskOffReentryUsedPct"))
    if protective <= reentry_used + 1e-9:
        return 0.0, ["RISK_OFF_REENTRY_NO_PROTECTIVE_CAPACITY"]
    last_protective_date = str(activity.get("lastProtectiveSellDate") or "")
    as_of_date = str(context.get("asOfDate") or "")
    if not last_protective_date:
        return 0.0, ["RISK_OFF_REENTRY_PROTECTIVE_EVENT_MISSING"]
    if last_protective_date >= as_of_date:
        return 0.0, ["RISK_OFF_REENTRY_SAME_DAY_FORBIDDEN"]
    if last_protective_date[:7] != as_of_date[:7]:
        return 0.0, ["RISK_OFF_REENTRY_EVENT_OUTSIDE_CURRENT_MONTH"]
    if factor_state.get("dataComplete") is not True:
        return 0.0, ["RISK_OFF_REENTRY_FACTOR_DATA_INCOMPLETE"]
    positive_count = int(number(factor_state.get("positiveFactorCount")))
    minimum_positive = int(number(config.get("minimumPositiveFactorCount"), 4))
    if positive_count < minimum_positive:
        return 0.0, [
            "RISK_OFF_REENTRY_FACTORS_NOT_CONFIRMED",
            f"POSITIVE_FACTOR_COUNT_{positive_count}",
        ]
    allowed_directions = {str(item) for item in config.get("allowedAiDirections") or []}
    direction = str(view.get("direction") or "")
    if direction not in allowed_directions:
        return 0.0, ["RISK_OFF_REENTRY_AI_DIRECTION_NOT_CONFIRMED", f"AI_DIRECTION_{direction or 'MISSING'}"]
    confidence = number(view.get("confidence"))
    minimum_confidence = number(config.get("minimumAiConfidence"), 1)
    if confidence + 1e-9 < minimum_confidence:
        return 0.0, ["RISK_OFF_REENTRY_AI_CONFIDENCE_TOO_LOW"]
    monthly_cap = number(config.get("maxMonthlyReentryPct"))
    capacity = min(max(0.0, monthly_cap - reentry_used), max(0.0, protective - reentry_used))
    if capacity <= 0:
        return 0.0, ["RISK_OFF_REENTRY_BUDGET_EXHAUSTED"]
    return capacity, [
        "RISK_OFF_REENTRY_SEPARATE_BUDGET",
        "USER_CLASSIFIED_PROTECTIVE_SELL",
        f"POSITIVE_FACTOR_COUNT_{positive_count}",
        f"AI_DIRECTION_{direction}",
    ]


def tactical_targets(
    policy: dict[str, Any],
    ai_view: dict[str, Any],
    *,
    risk_breached: bool,
    review_due: bool,
) -> tuple[dict[str, float], dict[str, float]]:
    sleeves, cash_id = index_policy(policy)
    views = ai_view_by_sleeve(ai_view)
    deltas: dict[str, float] = {}
    for sleeve_id, sleeve in sleeves.items():
        if sleeve_id == cash_id:
            continue
        view = views.get(sleeve_id) or {}
        confidence = number(view.get("confidence"))
        scale = 0.0 if confidence < 0.55 else 0.5 if confidence < 0.70 else 1.0
        budget = number(sleeve.get("tacticalBudgetPct"))
        proposed = clamp(number(view.get("proposedDeltaPct")), -budget, budget) * scale
        if str(view.get("direction") or "NEUTRAL") == "NEUTRAL":
            proposed = 0.0
        if (review_due or risk_breached) and number(sleeve.get("riskLevel")) > 0:
            proposed = min(0.0, proposed)
        deltas[sleeve_id] = proposed

    base_cash = number(sleeves[cash_id].get("targetWeightPct"))
    desired_cash = base_cash - sum(deltas.values())
    cash_min = number(sleeves[cash_id].get("minWeightPct"))
    cash_max = number(sleeves[cash_id].get("maxWeightPct"))
    if desired_cash < cash_min or desired_cash > cash_max:
        total_delta = sum(deltas.values())
        allowed_total = base_cash - clamp(desired_cash, cash_min, cash_max)
        scale = allowed_total / total_delta if abs(total_delta) > 1e-9 else 0.0
        scale = clamp(scale, 0.0, 1.0)
        deltas = {key: value * scale for key, value in deltas.items()}

    targets = {}
    for sleeve_id, sleeve in sleeves.items():
        if sleeve_id == cash_id:
            continue
        target = number(sleeve.get("targetWeightPct")) + deltas.get(sleeve_id, 0.0)
        targets[sleeve_id] = clamp(
            target,
            number(sleeve.get("minWeightPct")),
            number(sleeve.get("maxWeightPct")),
        )
    if risk_breached:
        for sleeve_id, sleeve in sleeves.items():
            if sleeve_id != cash_id and number(sleeve.get("riskLevel")) >= 3:
                targets[sleeve_id] = number(sleeve.get("minWeightPct"))

    limits = policy.get("portfolioLimits") or {}
    for limit_field in ("maxEquityWeightPct", "maxThemeWeightPct"):
        relevant = [
            sleeve_id for sleeve_id, sleeve in sleeves.items()
            if sleeve_matches_portfolio_limit(sleeve, limit_field)
        ]
        cap = number(limits.get(limit_field), 100)
        excess = sum(targets.get(item, 0) for item in relevant) - cap
        if excess > 1e-9:
            for sleeve_id in sorted(relevant, key=lambda key: targets.get(key, 0), reverse=True):
                minimum = number(sleeves[sleeve_id].get("minWeightPct"))
                reducible = max(0.0, targets[sleeve_id] - minimum)
                reduction = min(reducible, excess)
                targets[sleeve_id] -= reduction
                excess -= reduction
                if excess <= 1e-9:
                    break
    targets[cash_id] = 100.0 - sum(targets.values())
    effective_deltas = {
        sleeve_id: targets[sleeve_id] - number(sleeves[sleeve_id].get("targetWeightPct"))
        for sleeve_id in targets
    }
    return targets, effective_deltas


def post_pending_values(context: dict[str, Any]) -> tuple[dict[str, float], dict[str, str], list[dict[str, Any]], float]:
    holdings = context.get("portfolio", {}).get("holdings") or []
    values = {str(item.get("code")): max(0.0, number(item.get("marketValue"))) for item in holdings if item.get("code")}
    names = {str(item.get("code")): str(item.get("name") or item.get("code")) for item in holdings if item.get("code")}
    pending = [item for item in (context.get("pendingTransactions") or {}).get("items") or [] if isinstance(item, dict)]
    pending_sell_cash = 0.0
    for item in pending:
        code = str(item.get("code") or "")
        amount = max(0.0, number(item.get("amount")))
        if not code or amount <= 0:
            continue
        names.setdefault(code, str(item.get("name") or code))
        if item.get("type") == "BUY":
            values[code] = values.get(code, 0.0) + amount
        elif item.get("type") == "SELL":
            sold = min(values.get(code, 0.0), amount)
            values[code] = max(0.0, values.get(code, 0.0) - sold)
            pending_sell_cash += sold
    return values, names, pending, pending_sell_cash


def cash_value(payload: dict[str, Any], context: dict[str, Any]) -> tuple[float | None, list[str]]:
    cash = payload.get("cash")
    errors: list[str] = []
    if not isinstance(cash, dict):
        return None, ["FREE_CASH_NOT_CONFIRMED"]
    if cash.get("source") != "user_confirmed":
        errors.append("FREE_CASH_SOURCE_NOT_USER_CONFIRMED")
    if cash.get("asOfDate") != context.get("asOfDate"):
        errors.append("FREE_CASH_AS_OF_MISMATCH")
    if cash.get("excludesPendingBuys") is not True:
        errors.append("FREE_CASH_PENDING_BUY_SEMANTICS_INVALID")
    raw = cash.get("availableCny")
    if isinstance(raw, bool):
        errors.append("FREE_CASH_INVALID")
    try:
        available = float(raw)
        if not math.isfinite(available) or available < 0:
            raise ValueError
    except (TypeError, ValueError):
        available = 0.0
        errors.append("FREE_CASH_INVALID")
    return (available if not errors else None), errors


def drawdown_state(
    policy: dict[str, Any],
    context: dict[str, Any],
    total_assets: float,
) -> tuple[dict[str, Any] | None, list[str]]:
    """Resolve the policy-confirmed drawdown denominator without giving AI numeric authority."""
    basis = policy.get("drawdownBasis") if isinstance(policy.get("drawdownBasis"), dict) else {}
    scope = str(basis.get("scope") or "")
    method = str(basis.get("method") or "")
    risk = context.get("portfolio", {}).get("risk") or {}
    errors: list[str] = []
    if risk.get("complete") is not True:
        errors.append("DRAWDOWN_DATA_INCOMPLETE")
    raw_drawdown = risk.get("currentDrawdownPct")
    if isinstance(raw_drawdown, bool) or raw_drawdown is None:
        errors.append("MCP_DRAWDOWN_INVALID")
        source_drawdown = 0.0
    else:
        try:
            source_drawdown = float(raw_drawdown)
            if not math.isfinite(source_drawdown) or not 0 <= source_drawdown < 100:
                raise ValueError
        except (TypeError, ValueError):
            source_drawdown = 0.0
            errors.append("MCP_DRAWDOWN_INVALID")
    if errors:
        return None, list(dict.fromkeys(errors))

    policy_limit = min(
        number((policy.get("riskCapacity") or {}).get("maxDrawdownPct"), 100),
        number((policy.get("riskTolerance") or {}).get("maxDrawdownPct"), 100),
    )
    configured_limit = risk.get("configuredMaxDrawdownLimitPct")
    if scope == DRAWDOWN_SCOPE_MCP and method == DRAWDOWN_METHOD_MCP:
        if configured_limit is not None and abs(number(configured_limit) - policy_limit) > 0.1:
            return None, ["DRAWDOWN_LIMIT_CONFLICT_REQUIRES_POLICY_REVIEW"]
        return {
            "scope": scope,
            "method": method,
            "source": "context.portfolio.risk.currentDrawdownPct",
            "sourceScope": DRAWDOWN_SCOPE_MCP,
            "sourceDrawdownPct": source_drawdown,
            "effectiveDrawdownPct": source_drawdown,
            "totalInvestableAssetsCny": total_assets,
            "mcpFundPortfolioValueCny": number(context.get("portfolio", {}).get("totalMarketValue")),
            "nonMcpAssetsCny": max(
                0.0,
                total_assets - number(context.get("portfolio", {}).get("totalMarketValue")),
            ),
            "isApproximation": False,
            "assumption": None,
            "assumptions": [],
            "configuredMcpLimitPct": configured_limit,
        }, []

    if scope != DRAWDOWN_SCOPE_TOTAL or method != DRAWDOWN_METHOD_TOTAL_PROXY:
        return None, ["DRAWDOWN_BASIS_UNSUPPORTED"]
    raw_fund_value = context.get("portfolio", {}).get("totalMarketValue")
    if isinstance(raw_fund_value, bool) or raw_fund_value is None:
        return None, ["MCP_FUND_PORTFOLIO_VALUE_INVALID"]
    try:
        fund_value = float(raw_fund_value)
        if not math.isfinite(fund_value) or fund_value < 0:
            raise ValueError
    except (TypeError, ValueError):
        return None, ["MCP_FUND_PORTFOLIO_VALUE_INVALID"]
    mismatch_tolerance = max(0.01, total_assets * 0.0001)
    if fund_value > total_assets + mismatch_tolerance:
        return None, ["DRAWDOWN_BASIS_ASSET_MISMATCH"]
    non_mcp_assets = max(0.0, total_assets - fund_value)
    if fund_value <= 0 and source_drawdown > 0:
        return None, ["DRAWDOWN_BASIS_ASSET_MISMATCH"]
    drawdown_fraction = source_drawdown / 100.0
    fund_peak_proxy = fund_value / (1.0 - drawdown_fraction)
    total_peak_proxy = fund_peak_proxy + non_mcp_assets
    effective_drawdown = (
        (total_peak_proxy - total_assets) / total_peak_proxy * 100.0
        if total_peak_proxy > 0
        else 0.0
    )
    return {
        "scope": scope,
        "method": method,
        "source": "context.portfolio.risk.currentDrawdownPct",
        "sourceScope": DRAWDOWN_SCOPE_MCP,
        "sourceDrawdownPct": source_drawdown,
        "effectiveDrawdownPct": effective_drawdown,
        "totalInvestableAssetsCny": total_assets,
        "mcpFundPortfolioValueCny": fund_value,
        "nonMcpAssetsCny": non_mcp_assets,
        "fundPeakValueProxyCny": fund_peak_proxy,
        "totalPeakValueProxyCny": total_peak_proxy,
        "isApproximation": True,
        "assumption": "NON_MCP_ASSETS_CONSTANT_SINCE_MCP_FUND_PEAK",
        "assumptions": [
            "NON_MCP_ASSETS_CONSTANT_SINCE_MCP_FUND_PEAK",
            "MCP_LINKED_RETURN_DRAWDOWN_APPLIED_TO_CURRENT_FUND_VALUE",
        ],
        "configuredMcpLimitPct": configured_limit,
    }, []


def activity_state(payload: dict[str, Any], context: dict[str, Any]) -> tuple[dict[str, Any] | None, list[str]]:
    activity = payload.get("activity")
    errors: list[str] = []
    if not isinstance(activity, dict):
        return None, ["MONTHLY_TURNOVER_NOT_PROVIDED"]
    schema_version = activity.get("schemaVersion")
    allowed_sources = (
        {"classified_transaction_ledger", "strategy_ledger"}
        if schema_version == ACTIVITY_SCHEMA_V2
        else {"get_transaction_ledger", "strategy_ledger"}
    )
    if activity.get("source") not in allowed_sources:
        errors.append("MONTHLY_TURNOVER_SOURCE_INVALID")
    if activity.get("asOfDate") != context.get("asOfDate"):
        errors.append("MONTHLY_TURNOVER_AS_OF_MISMATCH")
    if schema_version != ACTIVITY_SCHEMA_V2:
        raw = activity.get("monthlyTurnoverUsedPct")
        if isinstance(raw, bool):
            errors.append("MONTHLY_TURNOVER_INVALID")
        try:
            used = float(raw)
            if not math.isfinite(used) or used < 0:
                raise ValueError
        except (TypeError, ValueError):
            used = 0.0
            errors.append("MONTHLY_TURNOVER_INVALID")
        state = {
            "schemaVersion": "portfolio_activity.legacy",
            "grossMonthlyTurnoverUsedPct": used,
            "ordinaryMonthlyTurnoverUsedPct": used,
            "protectiveSellTurnoverPct": 0.0,
            "riskOffReentryUsedPct": 0.0,
            "lastProtectiveSellDate": None,
        }
        return (state if not errors else None), errors

    fields = (
        "grossMonthlyTurnoverUsedPct",
        "ordinaryMonthlyTurnoverUsedPct",
        "protectiveSellTurnoverPct",
        "riskOffReentryUsedPct",
    )
    parsed: dict[str, float] = {}
    for field in fields:
        raw = activity.get(field)
        if isinstance(raw, bool):
            errors.append(f"ACTIVITY_V2_{field}_INVALID")
            parsed[field] = 0.0
            continue
        try:
            value = float(raw)
            if not math.isfinite(value) or value < 0:
                raise ValueError
            parsed[field] = value
        except (TypeError, ValueError):
            parsed[field] = 0.0
            errors.append(f"ACTIVITY_V2_{field}_INVALID")
    classified_sum = (
        parsed["ordinaryMonthlyTurnoverUsedPct"]
        + parsed["protectiveSellTurnoverPct"]
        + parsed["riskOffReentryUsedPct"]
    )
    if abs(parsed["grossMonthlyTurnoverUsedPct"] - classified_sum) > 0.02:
        errors.append("ACTIVITY_V2_BUCKETS_DO_NOT_SUM_TO_GROSS")

    events = activity.get("classificationEvents")
    if not isinstance(events, list):
        events = []
        errors.append("ACTIVITY_V2_CLASSIFICATION_EVENTS_REQUIRED")
    seen_event_ids: set[str] = set()
    seen_transaction_ids: set[str] = set()
    event_turnover = {"PROTECTIVE_SELL": 0.0, "RISK_OFF_REENTRY": 0.0}
    last_protective_date: str | None = None
    for index, event in enumerate(events):
        if not isinstance(event, dict):
            errors.append(f"ACTIVITY_V2_EVENT_{index}_INVALID")
            continue
        event_id = str(event.get("eventId") or "").strip()
        if not event_id or event_id in seen_event_ids:
            errors.append(f"ACTIVITY_V2_EVENT_{index}_ID_MISSING_OR_DUPLICATE")
        seen_event_ids.add(event_id)
        kind = str(event.get("kind") or "")
        if kind not in event_turnover:
            errors.append(f"ACTIVITY_V2_EVENT_{index}_KIND_INVALID")
            continue
        trade_date = str(event.get("tradeDate") or "")
        if not trade_date or trade_date > str(context.get("asOfDate") or ""):
            errors.append(f"ACTIVITY_V2_EVENT_{index}_DATE_INVALID")
        elif trade_date[:7] != str(context.get("asOfDate") or "")[:7]:
            errors.append(f"ACTIVITY_V2_EVENT_{index}_OUTSIDE_CURRENT_MONTH")
        if kind == "PROTECTIVE_SELL" and trade_date:
            last_protective_date = max(last_protective_date or trade_date, trade_date)
        if event.get("classificationSource") not in {"USER_CONFIRMED", "STRATEGY_DECISION"}:
            errors.append(f"ACTIVITY_V2_EVENT_{index}_SOURCE_INVALID")
        transaction_ids = event.get("transactionIds")
        if not isinstance(transaction_ids, list) or not transaction_ids:
            errors.append(f"ACTIVITY_V2_EVENT_{index}_TRANSACTIONS_REQUIRED")
        else:
            for transaction_id in transaction_ids:
                normalized = str(transaction_id or "").strip()
                if not normalized or normalized in seen_transaction_ids:
                    errors.append(f"ACTIVITY_V2_EVENT_{index}_TRANSACTION_MISSING_OR_DUPLICATE")
                seen_transaction_ids.add(normalized)
        turnover = number(event.get("turnoverPct"), -1)
        if turnover < 0:
            errors.append(f"ACTIVITY_V2_EVENT_{index}_TURNOVER_INVALID")
        else:
            event_turnover[kind] += turnover
    if abs(event_turnover["PROTECTIVE_SELL"] - parsed["protectiveSellTurnoverPct"]) > 0.02:
        errors.append("ACTIVITY_V2_PROTECTIVE_EVENTS_MISMATCH")
    if abs(event_turnover["RISK_OFF_REENTRY"] - parsed["riskOffReentryUsedPct"]) > 0.02:
        errors.append("ACTIVITY_V2_REENTRY_EVENTS_MISMATCH")
    state = {
        "schemaVersion": ACTIVITY_SCHEMA_V2,
        **parsed,
        "lastProtectiveSellDate": last_protective_date,
    }
    return (state if not errors else None), list(dict.fromkeys(errors))


def readiness_map(context: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {
        str(item.get("code")): item
        for item in (context.get("actionReadiness") or {}).get("funds") or []
        if isinstance(item, dict) and item.get("code")
    }


def holding_map(context: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {
        str(item.get("code")): item
        for item in context.get("portfolio", {}).get("holdings") or []
        if isinstance(item, dict) and item.get("code")
    }


def choose_fund(
    sleeve_id: str,
    side: str,
    sleeves: dict[str, dict[str, Any]],
    values: dict[str, float],
    ai_view: dict[str, Any],
) -> str | None:
    approved = [str(code) for code in sleeves[sleeve_id].get("approvedFundCodes") or []]
    view = ai_view_by_sleeve(ai_view).get(sleeve_id) or {}
    preferred_field = "preferredFundCodes" if side == "BUY" else "reduceFundCodes"
    preferred = [str(code) for code in view.get(preferred_field) or []]
    candidates = [code for code in preferred if code in approved and values.get(code, 0) > 0]
    if side == "BUY" and not candidates:
        return None
    if not candidates:
        candidates = [code for code in approved if values.get(code, 0) > 0]
    if not candidates:
        return None
    return max(candidates, key=lambda code: values.get(code, 0)) if side == "SELL" else candidates[0]


def side_is_ready(context: dict[str, Any], code: str, side: str) -> tuple[bool, list[str]]:
    item = readiness_map(context).get(code) or {}
    key = "buyReady" if side == "BUY" else "sellReady"
    reason_key = "buyReasons" if side == "BUY" else "sellReasons"
    reasons = [str(value) for value in item.get(reason_key) or []]
    return item.get(key) is True, reasons or (["FUND_SIDE_READINESS_MISSING"] if not item else [])


def constraint_caps(context: dict[str, Any], code: str, side: str) -> tuple[dict[str, float], list[str]]:
    holding = holding_map(context).get(code) or {}
    constraints = holding.get("tradeConstraints") if isinstance(holding.get("tradeConstraints"), dict) else {}
    errors: list[str] = []
    if not constraints.get("available"):
        errors.append("TRADE_CONSTRAINTS_UNAVAILABLE")
    if side == "BUY":
        status = str(constraints.get("purchaseStatus") or "")
        if not status or any(word in status for word in BLOCKED_PURCHASE_WORDS):
            errors.append("PURCHASE_NOT_AVAILABLE")
        daily_limit = number(constraints.get("dailyPurchaseLimit"), math.inf)
        if daily_limit <= 0:
            daily_limit = math.inf if not constraints.get("dailyPurchaseLimited") else 0.0
        minimum = max(0.0, number(constraints.get("minimumPurchaseAmount")))
        return {"dailyPurchaseLimit": daily_limit, "minimumPurchaseAmount": minimum}, errors
    status = str(constraints.get("redemptionStatus") or "")
    if not status or any(word in status for word in BLOCKED_REDEMPTION_WORDS):
        errors.append("REDEMPTION_NOT_AVAILABLE")
    return {}, errors


def pending_same_side(pending: list[dict[str, Any]], code: str, side: str) -> bool:
    return any(str(item.get("code")) == code and str(item.get("type")) == side for item in pending)


def blocked_candidate(
    payload: dict[str, Any],
    policy: dict[str, Any],
    context: dict[str, Any],
    blockers: list[str],
    *,
    scope: str | None = None,
    fund_code: str | None = None,
    fund_name: str | None = None,
    current_weight: float | None = None,
    target_weight: float | None = None,
    band: list[float | None] | None = None,
    drivers: list[str] | None = None,
    allocation: dict[str, Any] | None = None,
) -> dict[str, Any]:
    result = base_result("BLOCKED", "BLOCKED", blockers)
    result.update({
        "executionMode": str(policy.get("status") or "NONE"),
        "scope": scope,
        "fundCode": fund_code,
        "fundName": fund_name,
        "currentWeightPct": current_weight,
        "targetWeightPct": target_weight,
        "targetBandPct": band or [None, None],
        "drivers": drivers or [],
        "allocation": allocation or {},
        "dataAsOf": context.get("asOfDate"),
        "nextReviewAt": policy.get("nextReviewAt") or (context.get("execution") or {}).get("nextTradingDay"),
    })
    result["audit"].update({
        "policyVersion": policy.get("policyVersion"),
        "contextHash": (context.get("audit") or {}).get("contextHash") or context.get("contextHash"),
    })
    return finish(result, payload)


def confidence_label(view: dict[str, Any]) -> str:
    confidence = number(view.get("confidence"))
    return "HIGH" if confidence >= 0.75 else "MEDIUM" if confidence >= 0.60 else "LOW"


def decide(payload: dict[str, Any]) -> dict[str, Any]:
    policy = payload.get("policy") if isinstance(payload.get("policy"), dict) else None
    if not policy or policy.get("status") == "DRAFT":
        return needs_profile(policy, payload)
    policy_errors = validate_policy(policy)
    if policy_errors:
        result = base_result(
            "NEEDS_PROFILE",
            "NEEDS_PROFILE",
            [f"POLICY_INVALID:{item}" for item in policy_errors],
        )
        result["nextQuestion"] = next_question(policy)
        return finish(result, payload)
    if policy.get("status") == "SUSPENDED":
        return finish(base_result("BLOCKED", "BLOCKED", ["POLICY_SUSPENDED"]), payload)

    context = payload.get("context") if isinstance(payload.get("context"), dict) else {}
    if context.get("schemaVersion") != CONTEXT_SCHEMA:
        return finish(base_result("MCP_VERSION_BLOCKED", "MCP_VERSION_BLOCKED", ["QUANT_CONTEXT_V2_REQUIRED"]), payload)
    if context.get("readyForAnalysis") is not True:
        blockers = [str(item) for item in context.get("blockingReasons") or []] or ["CONTEXT_NOT_READY_FOR_ANALYSIS"]
        return finish(base_result("DATA_BLOCKED", "DATA_BLOCKED", blockers), payload)

    ai_view = payload.get("aiView") if isinstance(payload.get("aiView"), dict) else {}
    ai_errors = validate_ai_view(ai_view, policy, context)
    if ai_errors:
        return finish(base_result("AI_MODEL_BLOCKED", "AI_MODEL_BLOCKED", ai_errors), payload)

    free_cash, cash_errors = cash_value(payload, context)
    if cash_errors:
        return blocked_candidate(payload, policy, context, cash_errors)
    assert free_cash is not None

    sleeves, cash_id = index_policy(policy)
    mapping = {str(key): str(value) for key, value in (policy.get("fundSleeveMap") or {}).items()}
    values, names, pending, pending_sell_cash = post_pending_values(context)
    unmapped = [code for code, value in values.items() if value > 0.01 and code not in mapping]
    if unmapped:
        return blocked_candidate(payload, policy, context, [f"UNMAPPED_HOLDING:{code}" for code in unmapped])

    sleeve_values = {sleeve_id: 0.0 for sleeve_id in sleeves}
    for code, value in values.items():
        sleeve_id = mapping.get(code)
        if sleeve_id:
            sleeve_values[sleeve_id] += value
    sleeve_values[cash_id] += free_cash + pending_sell_cash
    total_assets = sum(sleeve_values.values())
    if total_assets <= 0:
        return blocked_candidate(payload, policy, context, ["TOTAL_INVESTABLE_ASSETS_UNAVAILABLE"])
    current_weights = {key: value / total_assets * 100 for key, value in sleeve_values.items()}
    current_fund_weights = {code: value / total_assets * 100 for code, value in values.items()}
    factor_states = sleeve_factor_states(policy, context, values)

    policy_limit = min(
        number((policy.get("riskCapacity") or {}).get("maxDrawdownPct"), 100),
        number((policy.get("riskTolerance") or {}).get("maxDrawdownPct"), 100),
    )
    drawdown_basis, drawdown_errors = drawdown_state(policy, context, total_assets)
    if drawdown_errors:
        return blocked_candidate(payload, policy, context, drawdown_errors)
    assert drawdown_basis is not None
    drawdown = number(drawdown_basis.get("effectiveDrawdownPct"))
    risk_breached = policy_limit > 0 and drawdown >= policy_limit
    risk_controls = policy.get("riskControls") if isinstance(policy.get("riskControls"), dict) else {}
    soft_trigger = number(risk_controls.get("softDrawdownTriggerPct"))
    soft_trigger_crossed = (
        risk_controls.get("softTriggerMode") == "DOWNTREND_FACTORS"
        and soft_trigger > 0
        and drawdown >= soft_trigger
        and not risk_breached
    )
    review_due = policy.get("status") == "REVIEW_DUE"
    targets, tactical_deltas = tactical_targets(
        policy,
        ai_view,
        risk_breached=risk_breached,
        review_due=review_due,
    )
    soft_risk_sleeve: str | None = None
    soft_reduction_step = 0.0
    if soft_trigger_crossed:
        targets, soft_risk_sleeve, soft_reduction_step = soft_risk_adjustment(
            policy,
            current_weights,
            targets,
            factor_states,
        )
        tactical_deltas = {
            sleeve_id: targets[sleeve_id] - number(sleeves[sleeve_id].get("targetWeightPct"))
            for sleeve_id in targets
        }

    if review_due and not risk_breached:
        return blocked_candidate(
            payload,
            policy,
            context,
            ["POLICY_REVIEW_DUE"],
            drivers=["NEW_RISK_SUSPENDED_UNTIL_POLICY_RECONFIRMED"],
        )

    gaps_pct = {key: targets[key] - current_weights.get(key, 0.0) for key in targets}
    risky_overweights = [
        key for key, sleeve in sleeves.items()
        if key != cash_id and number(sleeve.get("riskLevel")) >= 3 and gaps_pct.get(key, 0) < -0.01
    ]
    side = ""
    scope = ""
    action = "HOLD"
    drivers: list[str] = []
    forced_code: str | None = None
    forced_gap_pct: float | None = None
    limits = policy.get("portfolioLimits") or {}
    aggregate_breaches: list[tuple[float, str, str]] = []
    for limit_field in ("maxThemeWeightPct", "maxEquityWeightPct"):
        relevant = [
            sleeve_id
            for sleeve_id, sleeve in sleeves.items()
            if sleeve_matches_portfolio_limit(sleeve, limit_field)
        ]
        excess = sum(current_weights.get(sleeve_id, 0.0) for sleeve_id in relevant) - number(
            limits.get(limit_field),
            100,
        )
        reducible = [sleeve_id for sleeve_id in relevant if gaps_pct.get(sleeve_id, 0.0) < -0.01]
        if excess > 0.01 and reducible:
            breached_scope = min(reducible, key=lambda sleeve_id: gaps_pct[sleeve_id])
            aggregate_breaches.append((excess, limit_field, breached_scope))
    single_limit = number(limits.get("maxSingleFundWeightPct"), 100)
    single_overweights = [
        code for code, weight in current_fund_weights.items()
        if weight > single_limit + 0.01 and mapping.get(code) in sleeves
    ]
    if risk_breached and risky_overweights:
        side = "SELL"
        scope = min(risky_overweights, key=lambda key: gaps_pct[key])
        action = "RISK_REDUCE"
        drivers = ["PORTFOLIO_DRAWDOWN_ABOVE_POLICY", "RISKY_SLEEVE_ABOVE_REDUCED_TARGET"]
    elif soft_risk_sleeve and gaps_pct.get(soft_risk_sleeve, 0) < -0.01:
        side = "SELL"
        scope = soft_risk_sleeve
        action = "RISK_REDUCE"
        drivers = [
            "PORTFOLIO_DRAWDOWN_ABOVE_SOFT_TRIGGER",
            "DOWNTREND_FACTORS_CONFIRMED",
            "DYNAMIC_RISK_REDUCTION_STEP",
        ]
    elif aggregate_breaches:
        excess, limit_field, scope = max(aggregate_breaches)
        side = "SELL"
        action = "STRATEGIC_REBALANCE"
        forced_gap_pct = min(excess, abs(gaps_pct.get(scope, 0.0)))
        drivers = [
            "AGGREGATE_PORTFOLIO_LIMIT_BREACHED",
            "THEME_WEIGHT_ABOVE_POLICY" if limit_field == "maxThemeWeightPct" else "EQUITY_WEIGHT_ABOVE_POLICY",
        ]
    elif single_overweights:
        forced_code = max(single_overweights, key=lambda code: current_fund_weights[code] - single_limit)
        scope = mapping[forced_code]
        side = "SELL"
        action = "STRATEGIC_REBALANCE"
        forced_gap_pct = current_fund_weights[forced_code] - single_limit
        drivers = ["SINGLE_FUND_WEIGHT_ABOVE_POLICY"]
    else:
        cash_excess_pct = current_weights.get(cash_id, 0.0) - targets.get(cash_id, 0.0)
        underweights = [key for key in sleeves if key != cash_id and gaps_pct.get(key, 0) > 0.01]
        if cash_excess_pct > 0.01 and underweights:
            side = "BUY"
            scope = max(underweights, key=lambda key: gaps_pct[key])
            action = "TACTICAL_ROTATE" if abs(tactical_deltas.get(scope, 0.0)) > 0.01 else "CONTRIBUTION_REBALANCE"
            drivers = ["SLEEVE_UNDERWEIGHT", "FREE_CASH_ABOVE_TARGET"]
            if action == "TACTICAL_ROTATE":
                drivers.append("AI_TACTICAL_VIEW_WITHIN_POLICY")
        else:
            overweights = [
                key for key, sleeve in sleeves.items()
                if key != cash_id and current_weights.get(key, 0) > number(sleeve.get("maxWeightPct")) + 0.01
            ]
            if overweights:
                side = "SELL"
                scope = max(overweights, key=lambda key: current_weights[key] - targets[key])
                action = "STRATEGIC_REBALANCE"
                drivers = ["SLEEVE_ABOVE_POLICY_BAND"]

    allocation = {
        "totalInvestableAssetsCny": round(total_assets, 2),
        "currentWeightsPct": {key: round(value, 4) for key, value in current_weights.items()},
        "currentFundWeightsPct": {key: round(value, 4) for key, value in current_fund_weights.items()},
        "targetWeightsPct": {key: round(value, 4) for key, value in targets.items()},
        "tacticalDeltasPct": {key: round(value, 4) for key, value in tactical_deltas.items()},
        "effectiveMaxDrawdownPct": round(policy_limit, 4),
        "currentDrawdownPct": round(drawdown, 4),
        "sourceMcpDrawdownPct": round(number(drawdown_basis.get("sourceDrawdownPct")), 4),
        "riskControl": {
            "softDrawdownTriggerPct": round(soft_trigger, 4) if soft_trigger > 0 else None,
            "softTriggerCrossed": soft_trigger_crossed,
            "softRiskSleeve": soft_risk_sleeve,
            "softReductionStepPct": round(soft_reduction_step, 4),
            "hardLimitBreached": risk_breached,
            "factorMethod": risk_controls.get("factorMethod"),
            "drawdownBasis": {
                key: round(value, 4) if isinstance(value, float) else value
                for key, value in drawdown_basis.items()
            },
        },
        "factorStates": factor_states,
    }

    if not side:
        hold_status = "VALID" if policy.get("status") == "ACTIVE" else "SHADOW"
        result = base_result(hold_status, "HOLD")
        result.update({
            "executionMode": str(policy.get("status")),
            "drivers": ["PORTFOLIO_WITHIN_EFFECTIVE_TARGETS", "NO_MINIMUM_EFFECTIVE_TRADE"],
            "confidence": "MEDIUM",
            "dataAsOf": context.get("asOfDate"),
            "nextReviewAt": policy.get("nextReviewAt"),
            "allocation": allocation,
        })
        result["audit"].update({
            "policyVersion": policy.get("policyVersion"),
            "aiModelVersion": ai_view.get("modelVersion"),
            "aiPromptVersion": ai_view.get("promptVersion"),
            "evidenceSetHash": ai_view.get("evidenceSetHash"),
            "contextHash": (context.get("audit") or {}).get("contextHash") or context.get("contextHash"),
        })
        return finish(result, payload)

    code = forced_code or choose_fund(scope, side, sleeves, values, ai_view)
    if not code:
        blocker = "AI_FUND_SELECTION_MISSING" if side == "BUY" else "APPROVED_FUND_FOR_REDUCTION_MISSING"
        return blocked_candidate(
            payload, policy, context, [blocker],
            scope=scope,
            current_weight=round(current_weights.get(scope, 0), 4),
            target_weight=round(targets[scope], 4),
            band=[number(sleeves[scope].get("minWeightPct")), number(sleeves[scope].get("maxWeightPct"))],
            drivers=drivers,
            allocation=allocation,
        )

    view = ai_view_by_sleeve(ai_view).get(scope) or {}
    band = [number(sleeves[scope].get("minWeightPct")), number(sleeves[scope].get("maxWeightPct"))]
    common_fields = {
        "scope": scope,
        "fund_code": code,
        "fund_name": names.get(code, code),
        "current_weight": round(current_weights.get(scope, 0), 4),
        "target_weight": round(targets[scope], 4),
        "band": band,
        "drivers": drivers,
        "allocation": allocation,
    }
    if pending_same_side(pending, code, side):
        return blocked_candidate(payload, policy, context, ["DUPLICATE_PENDING_DIRECTION"], **common_fields)
    ready, ready_reasons = side_is_ready(context, code, side)
    caps, constraint_errors = constraint_caps(context, code, side)
    action_blockers = []
    if context.get("readyForAction") is not True:
        action_blockers.extend(str(item) for item in context.get("blockingReasons") or ["CONTEXT_NOT_READY_FOR_ACTION"])
    if (context.get("execution") or {}).get("actionable") is not True:
        action_blockers.append(str((context.get("execution") or {}).get("reason") or "EXECUTION_WINDOW_CLOSED"))
    if not ready:
        action_blockers.extend(ready_reasons)
    action_blockers.extend(constraint_errors)
    if action_blockers:
        return blocked_candidate(payload, policy, context, action_blockers, **common_fields)

    activity, activity_errors = activity_state(payload, context)
    if activity_errors:
        return blocked_candidate(payload, policy, context, activity_errors, **common_fields)
    assert activity is not None
    ordinary_turnover_used = number(activity.get("ordinaryMonthlyTurnoverUsedPct"))

    limits = policy.get("portfolioLimits") or {}
    raw_gap = (forced_gap_pct if forced_gap_pct is not None else abs(gaps_pct[scope])) / 100 * total_assets
    one_trade_cap = number(limits.get("maxOneTradeWeightPct")) / 100 * total_assets
    hard_monthly_turnover_remaining_pct = max(
        0.0,
        number(limits.get("maxMonthlyTurnoverPct")) - ordinary_turnover_used,
    )
    effective_turnover_limit_pct, turnover_drivers = effective_monthly_turnover_limit_pct(
        policy,
        action,
        side,
        factor_states.get(scope) or {},
        view,
    )
    turnover_exempt = effective_turnover_limit_pct is None
    if turnover_exempt:
        monthly_turnover_remaining_pct = math.inf
        monthly_turnover_cap = math.inf
    else:
        monthly_turnover_remaining_pct = max(0.0, effective_turnover_limit_pct - ordinary_turnover_used)
        monthly_turnover_cap = monthly_turnover_remaining_pct / 100 * total_assets
    reentry_capacity_pct = 0.0
    reentry_drivers: list[str] = []
    reentry_evaluated = False
    if (
        side == "BUY"
        and action in ORDINARY_BUY_ACTIONS
        and monthly_turnover_cap < number(limits.get("minTradeCny"))
    ):
        reentry_evaluated = True
        reentry_capacity_pct, reentry_drivers = risk_off_reentry_capacity_pct(
            policy,
            context,
            activity,
            factor_states.get(scope) or {},
            view,
        )
        if reentry_capacity_pct > 0:
            action = "REENTRY_AFTER_RISK_OFF"
            monthly_turnover_remaining_pct = reentry_capacity_pct
            monthly_turnover_cap = reentry_capacity_pct / 100 * total_assets
            turnover_exempt = False
            turnover_drivers = reentry_drivers
    step = number(limits.get("amountStepCny"), 1)
    min_trade = number(limits.get("minTradeCny"))
    amount_trace: dict[str, Any] = {
        "rawGapCny": round(raw_gap, 2),
        "oneTradeCapCny": round(one_trade_cap, 2),
        "hardMonthlyTurnoverRemainingCapCny": round(
            hard_monthly_turnover_remaining_pct / 100 * total_assets,
            2,
        ),
        "activitySchemaVersion": activity.get("schemaVersion"),
        "grossMonthlyTurnoverUsedPct": round(number(activity.get("grossMonthlyTurnoverUsedPct")), 4),
        "ordinaryMonthlyTurnoverUsedPct": round(ordinary_turnover_used, 4),
        "protectiveSellTurnoverPct": round(number(activity.get("protectiveSellTurnoverPct")), 4),
        "riskOffReentryUsedPct": round(number(activity.get("riskOffReentryUsedPct")), 4),
        "riskOffReentryRemainingPct": round(reentry_capacity_pct, 4),
        "riskOffReentryEvaluated": reentry_evaluated,
        "riskOffReentryEvaluation": reentry_drivers,
        "effectiveMonthlyTurnoverLimitPct": (
            None
            if turnover_exempt
            else round(
                number((risk_controls.get("riskOffReentry") or {}).get("maxMonthlyReentryPct"))
                if action == "REENTRY_AFTER_RISK_OFF"
                else effective_turnover_limit_pct,
                4,
            )
        ),
        "monthlyTurnoverRemainingCapCny": None if turnover_exempt else round(monthly_turnover_cap, 2),
        "monthlyTurnoverUsedPct": round(ordinary_turnover_used, 4),
        "monthlyTurnoverLimitExempt": turnover_exempt,
        "turnoverBudgetType": (
            "RISK_REDUCTION_EXEMPT"
            if turnover_exempt
            else "RISK_OFF_REENTRY"
            if action == "REENTRY_AFTER_RISK_OFF"
            else "ORDINARY"
        ),
        "turnoverDrivers": turnover_drivers,
        "amountStepCny": step,
    }
    if side == "BUY":
        single_cap = max(0.0, number(limits.get("maxSingleFundWeightPct")) / 100 * total_assets - values.get(code, 0))
        purchase_cap = caps.get("dailyPurchaseLimit", math.inf)
        effective_cap = min(raw_gap, free_cash, one_trade_cap, monthly_turnover_cap, single_cap, purchase_cap)
        amount = floor_step(effective_cap, step)
        required_minimum = max(min_trade, caps.get("minimumPurchaseAmount", 0.0))
        amount_trace.update({
            "availableCashCapCny": round(free_cash, 2),
            "singleFundCapacityCny": round(single_cap, 2),
            "purchaseLimitCapCny": None if math.isinf(purchase_cap) else round(purchase_cap, 2),
            "effectiveCapCny": round(effective_cap, 2),
            "minimumEffectiveTradeCny": round(required_minimum, 2),
        })
    else:
        fund_cap = values.get(code, 0.0)
        effective_cap = min(raw_gap, one_trade_cap, monthly_turnover_cap, fund_cap)
        amount = floor_step(effective_cap, step)
        required_minimum = min_trade
        amount_trace.update({
            "fundHoldingCapCny": round(fund_cap, 2),
            "effectiveCapCny": round(effective_cap, 2),
            "minimumEffectiveTradeCny": round(required_minimum, 2),
        })
    if amount < required_minimum or amount <= 0:
        hold_status = "VALID" if policy.get("status") == "ACTIVE" else "SHADOW"
        result = base_result(hold_status, "HOLD")
        result.update({
            "executionMode": str(policy.get("status")),
            "scope": scope,
            "fundCode": code,
            "fundName": names.get(code, code),
            "drivers": [*drivers, "BELOW_MINIMUM_EFFECTIVE_TRADE"],
            "confidence": confidence_label(view),
            "dataAsOf": context.get("asOfDate"),
            "nextReviewAt": policy.get("nextReviewAt"),
            "amountTrace": amount_trace,
            "allocation": allocation,
            "invalidationTriggers": view.get("invalidationTriggers") or [],
        })
    else:
        execution_mode = str(policy.get("status"))
        result = base_result("VALID" if execution_mode == "ACTIVE" else "SHADOW", action)
        result.update({
            "executionMode": execution_mode,
            "scope": scope,
            "fundCode": code,
            "fundName": names.get(code, code),
            "amountCny": round(amount, 2) if execution_mode == "ACTIVE" else None,
            "shadowAmountCny": round(amount, 2) if execution_mode != "ACTIVE" else None,
            "currentWeightPct": round(current_weights.get(scope, 0), 4),
            "targetWeightPct": round(targets[scope], 4),
            "targetBandPct": band,
            "changeWeightPct": round((amount / total_assets * 100) * (1 if side == "BUY" else -1), 4),
            "drivers": drivers,
            "confidence": confidence_label(view),
            "validUntil": f"{context.get('asOfDate')}T14:55:00+08:00" if execution_mode == "ACTIVE" else None,
            "nextReviewAt": policy.get("nextReviewAt") or (context.get("execution") or {}).get("nextTradingDay"),
            "dataAsOf": context.get("asOfDate"),
            "amountTrace": amount_trace,
            "allocation": allocation,
            "invalidationTriggers": view.get("invalidationTriggers") or [],
            "side": side,
        })
    result["audit"].update({
        "policyVersion": policy.get("policyVersion"),
        "aiModelVersion": ai_view.get("modelVersion"),
        "aiPromptVersion": ai_view.get("promptVersion"),
        "evidenceSetHash": ai_view.get("evidenceSetHash"),
        "contextHash": (context.get("audit") or {}).get("contextHash") or context.get("contextHash"),
    })
    result = finish(result, payload)
    violations = invariant_violations(result, payload)
    if violations:
        invalid = deepcopy(result)
        invalid["status"] = "INVALID_DECISION"
        invalid["action"] = "INVALID_DECISION"
        invalid["amountCny"] = None
        invalid["shadowAmountCny"] = None
        invalid["validUntil"] = None
        invalid["blockers"] = [f"INVARIANT:{item}" for item in violations]
        return finish(invalid, payload)
    return result


def invariant_violations(result: dict[str, Any], payload: dict[str, Any]) -> list[str]:
    violations: list[str] = []
    policy = payload.get("policy") or {}
    context = payload.get("context") or {}
    action = result.get("action")
    amount = result.get("amountCny")
    allocation = result.get("allocation") or {}
    targets = allocation.get("targetWeightsPct") or {}
    sleeves, _ = index_policy(policy) if policy.get("assetSleeves") else ({}, "")
    if targets:
        if abs(sum(number(value) for value in targets.values()) - 100.0) > 0.02:
            violations.append("TARGET_WEIGHTS_NOT_100")
        for sleeve_id, target in targets.items():
            sleeve = sleeves.get(sleeve_id) or {}
            if not number(sleeve.get("minWeightPct")) - 0.01 <= number(target) <= number(sleeve.get("maxWeightPct")) + 0.01:
                violations.append(f"TARGET_OUTSIDE_BAND:{sleeve_id}")
        limits = policy.get("portfolioLimits") or {}
        for limit_field in ("maxEquityWeightPct", "maxThemeWeightPct"):
            aggregate = sum(
                number(targets.get(sleeve_id))
                for sleeve_id, sleeve in sleeves.items()
                if sleeve_matches_portfolio_limit(sleeve, limit_field)
            )
            if aggregate > number(limits.get(limit_field), 100) + 0.01:
                violations.append(f"TARGET_EXCEEDS_{limit_field}")
    if result.get("executionMode") != "ACTIVE" and amount is not None:
        violations.append("NON_ACTIVE_AMOUNT_MUST_BE_NULL")
    if amount is not None:
        if number(amount) <= 0:
            violations.append("ACTION_AMOUNT_NOT_POSITIVE")
        if context.get("readyForAction") is not True or (context.get("execution") or {}).get("actionable") is not True:
            violations.append("ACTION_WITH_CLOSED_CONTEXT")
        trace = result.get("amountTrace") or {}
        for field in (
            "rawGapCny",
            "oneTradeCapCny",
            "monthlyTurnoverRemainingCapCny",
            "availableCashCapCny" if action in BUY_ACTIONS else "fundHoldingCapCny",
            "singleFundCapacityCny" if action in BUY_ACTIONS else None,
            "effectiveCapCny",
        ):
            if field and trace.get(field) is not None and number(amount) > number(trace.get(field)) + 0.011:
                violations.append(f"AMOUNT_EXCEEDS_{field}")
        if action in BUY_ACTIONS and trace.get("purchaseLimitCapCny") is not None and number(amount) > number(trace["purchaseLimitCapCny"]) + 0.011:
            violations.append("AMOUNT_EXCEEDS_PURCHASE_LIMIT")
        code = str(result.get("fundCode") or "")
        scope = str(result.get("scope") or "")
        if (policy.get("fundSleeveMap") or {}).get(code) != scope:
            violations.append("FUND_SCOPE_MAPPING_INVALID")
        if code not in [str(value) for value in (sleeves.get(scope) or {}).get("approvedFundCodes") or []]:
            violations.append("FUND_NOT_APPROVED")
        side = str(result.get("side") or "")
        if pending_same_side(
            [item for item in (context.get("pendingTransactions") or {}).get("items") or [] if isinstance(item, dict)],
            code,
            side,
        ):
            violations.append("DUPLICATE_PENDING_DIRECTION")
        ready, _ = side_is_ready(context, code, side)
        if not ready:
            violations.append("FUND_SIDE_NOT_READY")
    elif result.get("status") == "VALID" and action in BUY_ACTIONS | SELL_ACTIONS:
        violations.append("VALID_TRADE_ACTION_WITHOUT_AMOUNT")
    if result.get("status") in {"BLOCKED", "DATA_BLOCKED", "AI_MODEL_BLOCKED", "ENGINE_BLOCKED", "INVALID_DECISION"} and amount is not None:
        violations.append("BLOCKED_RESULT_HAS_AMOUNT")
    return list(dict.fromkeys(violations))
