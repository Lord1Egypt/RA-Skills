#!/usr/bin/env python3
"""Append-only, per-user investor policy store for hua-personal-strategy v4.3.0."""

from __future__ import annotations

import argparse
import contextlib
import hashlib
import json
import os
import re
import tempfile
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterator


POLICY_SCHEMA = "investor_policy.v1"
POLICY_STATUSES = {
    "DRAFT",
    "CONFIRMED",
    "SHADOW",
    "ACTIVE",
    "REVIEW_DUE",
    "SUSPENDED",
}
CONFIRMED_STATUSES = POLICY_STATUSES - {"DRAFT"}
FUND_CODE_RE = re.compile(r"^\d{6}$")


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def content_hash(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def default_state_root() -> Path:
    configured = os.environ.get("HUA_PERSONAL_STRATEGY_STATE_DIR")
    if configured:
        return Path(configured).expanduser().resolve()
    return Path.home() / ".local" / "share" / "hua-personal-strategy"


def user_key(user_id: str) -> str:
    normalized = str(user_id or "").strip()
    if not normalized:
        raise ValueError("user_id is required")
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()[:20]


def user_paths(root: Path, key: str) -> tuple[Path, Path, Path]:
    directory = root / "users" / key
    return directory / "current-policy.json", directory / "policy-events.jsonl", directory / ".lock"


@contextlib.contextmanager
def locked(lock_path: Path) -> Iterator[None]:
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    handle = lock_path.open("a+", encoding="utf-8")
    try:
        try:
            import fcntl

            fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
        except ImportError:
            pass
        yield
    finally:
        try:
            import fcntl

            fcntl.flock(handle.fileno(), fcntl.LOCK_UN)
        except ImportError:
            pass
        handle.close()


def load_current(root: Path, key: str) -> dict[str, Any] | None:
    current_path, _, _ = user_paths(root, key)
    if not current_path.exists():
        return None
    value = json.loads(current_path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("stored policy is not an object")
    return value


def _number(value: Any, field: str, errors: list[str], *, minimum: float = 0, maximum: float | None = None) -> float:
    if isinstance(value, bool):
        errors.append(f"{field}:must_be_number")
        return 0.0
    try:
        number = float(value)
    except (TypeError, ValueError):
        errors.append(f"{field}:must_be_number")
        return 0.0
    if number < minimum or (maximum is not None and number > maximum):
        errors.append(f"{field}:out_of_range")
    return number


def _counts_toward_limit(sleeve: dict[str, Any], limit_field: str) -> bool:
    asset_class = str(sleeve.get("assetClass") or "")
    if limit_field == "maxEquityWeightPct":
        return asset_class.startswith("EQUITY") or asset_class.startswith("THEME")
    if limit_field == "maxThemeWeightPct":
        return asset_class.startswith("THEME") or "_THEME" in asset_class
    return False


def validate_policy(policy: dict[str, Any], *, allow_draft: bool = False) -> list[str]:
    errors: list[str] = []
    if not isinstance(policy, dict):
        return ["policy:must_be_object"]
    if policy.get("schemaVersion") != POLICY_SCHEMA:
        errors.append("schemaVersion:must_equal_investor_policy.v1")
    status = str(policy.get("status") or "")
    if status not in POLICY_STATUSES:
        errors.append("status:invalid")
    if not isinstance(policy.get("policyVersion"), int) or int(policy.get("policyVersion") or 0) < 1:
        errors.append("policyVersion:must_be_positive_integer")
    if "userId" in policy or "uid" in policy:
        errors.append("policy:must_not_store_raw_user_id")
    if allow_draft and status == "DRAFT":
        return errors

    goals = policy.get("goals")
    if not isinstance(goals, list) or not goals:
        errors.append("goals:at_least_one_required")
    else:
        goal_ids: set[str] = set()
        for index, goal in enumerate(goals):
            if not isinstance(goal, dict):
                errors.append(f"goals[{index}]:must_be_object")
                continue
            goal_id = str(goal.get("id") or "").strip()
            if not goal_id or goal_id in goal_ids:
                errors.append(f"goals[{index}].id:missing_or_duplicate")
            goal_ids.add(goal_id)
            if not str(goal.get("purpose") or "").strip():
                errors.append(f"goals[{index}].purpose:required")
            if not str(goal.get("targetDate") or "").strip():
                errors.append(f"goals[{index}].targetDate:required")
            _number(goal.get("priority"), f"goals[{index}].priority", errors, minimum=1)
            target_amount_mode = goal.get("targetAmountMode")
            if target_amount_mode is None:
                if goal.get("targetAmountCny") is None:
                    errors.append(f"goals[{index}].targetAmountCny:required_or_use_NONE_mode")
            elif target_amount_mode not in {"FIXED", "NONE"}:
                errors.append(f"goals[{index}].targetAmountMode:invalid")
            elif target_amount_mode == "FIXED":
                _number(goal.get("targetAmountCny"), f"goals[{index}].targetAmountCny", errors, minimum=0.01)
            elif goal.get("targetAmountCny") is not None:
                errors.append(f"goals[{index}].targetAmountCny:must_be_null_for_NONE_mode")
            _number(
                goal.get("plannedContributionCnyPerMonth"),
                f"goals[{index}].plannedContributionCnyPerMonth",
                errors,
            )
            if goal.get("currentInvestableAssetsCny") is not None:
                _number(
                    goal.get("currentInvestableAssetsCny"),
                    f"goals[{index}].currentInvestableAssetsCny",
                    errors,
                )

    capacity = policy.get("riskCapacity") if isinstance(policy.get("riskCapacity"), dict) else {}
    tolerance = policy.get("riskTolerance") if isinstance(policy.get("riskTolerance"), dict) else {}
    capacity_drawdown = _number(
        capacity.get("maxDrawdownPct"),
        "riskCapacity.maxDrawdownPct",
        errors,
        minimum=0.1,
        maximum=60,
    )
    tolerance_drawdown = _number(
        tolerance.get("maxDrawdownPct"),
        "riskTolerance.maxDrawdownPct",
        errors,
        minimum=0.1,
        maximum=60,
    )
    if not isinstance(capacity.get("emergencyFundReady"), bool):
        errors.append("riskCapacity.emergencyFundReady:required_boolean")
    if str(tolerance.get("stressReaction") or "") not in {"ADD", "HOLD", "EXIT", "DYNAMIC_REDUCE"}:
        errors.append("riskTolerance.stressReaction:invalid")

    drawdown_basis = policy.get("drawdownBasis")
    if not isinstance(drawdown_basis, dict):
        errors.append("drawdownBasis:required_object")
    else:
        drawdown_scope = drawdown_basis.get("scope")
        drawdown_method = drawdown_basis.get("method")
        valid_drawdown_pairs = {
            ("MCP_FUND_PORTFOLIO", "MCP_REPORTED"),
            ("TOTAL_INVESTABLE_ASSETS", "STATIC_CASH_PROXY_V1"),
        }
        if (drawdown_scope, drawdown_method) not in valid_drawdown_pairs:
            errors.append("drawdownBasis:unsupported_scope_method_pair")

    risk_controls = policy.get("riskControls")
    risk_off_reentry: dict[str, Any] | None = None
    if tolerance.get("stressReaction") == "DYNAMIC_REDUCE" and not isinstance(risk_controls, dict):
        errors.append("riskControls:required_for_DYNAMIC_REDUCE")
    if risk_controls is not None:
        if not isinstance(risk_controls, dict):
            errors.append("riskControls:must_be_object")
            risk_controls = {}
        soft_trigger = _number(
            risk_controls.get("softDrawdownTriggerPct"),
            "riskControls.softDrawdownTriggerPct",
            errors,
            minimum=0.1,
            maximum=60,
        )
        effective_hard_limit = min(capacity_drawdown, tolerance_drawdown)
        if soft_trigger >= effective_hard_limit:
            errors.append("riskControls.softDrawdownTriggerPct:must_be_below_effective_hard_limit")
        if risk_controls.get("softTriggerMode") != "DOWNTREND_FACTORS":
            errors.append("riskControls.softTriggerMode:must_be_DOWNTREND_FACTORS")
        if risk_controls.get("factorMethod") != "fund_trend_consensus_v1":
            errors.append("riskControls.factorMethod:unsupported")
        minimum_adverse = risk_controls.get("minimumAdverseFactorCount")
        if isinstance(minimum_adverse, bool) or not isinstance(minimum_adverse, int) or not 1 <= minimum_adverse <= 4:
            errors.append("riskControls.minimumAdverseFactorCount:must_be_integer_1_to_4")
            minimum_adverse = 4
        reduction_steps = risk_controls.get("reductionStepPctByAdverseFactorCount")
        if not isinstance(reduction_steps, dict):
            errors.append("riskControls.reductionStepPctByAdverseFactorCount:must_be_object")
        else:
            for factor_count in range(int(minimum_adverse), 5):
                field = f"riskControls.reductionStepPctByAdverseFactorCount.{factor_count}"
                if str(factor_count) not in reduction_steps:
                    errors.append(f"{field}:required")
                    continue
                _number(reduction_steps[str(factor_count)], field, errors, minimum=0.1, maximum=20)
        dynamic_turnover = risk_controls.get("dynamicTurnover")
        if not isinstance(dynamic_turnover, dict):
            errors.append("riskControls.dynamicTurnover:must_be_object")
        else:
            if not isinstance(dynamic_turnover.get("enabled"), bool):
                errors.append("riskControls.dynamicTurnover.enabled:required_boolean")
            if dynamic_turnover.get("factorMethod") != "fund_trend_consensus_v1":
                errors.append("riskControls.dynamicTurnover.factorMethod:unsupported")
            _number(
                dynamic_turnover.get("tierStepPct"),
                "riskControls.dynamicTurnover.tierStepPct",
                errors,
                minimum=0.1,
                maximum=20,
            )
            minimum_confirming = dynamic_turnover.get("minimumConfirmingFactorCount")
            if (
                isinstance(minimum_confirming, bool)
                or not isinstance(minimum_confirming, int)
                or not 1 <= minimum_confirming <= 4
            ):
                errors.append("riskControls.dynamicTurnover.minimumConfirmingFactorCount:must_be_integer_1_to_4")
            if not isinstance(dynamic_turnover.get("riskReductionExempt"), bool):
                errors.append("riskControls.dynamicTurnover.riskReductionExempt:required_boolean")
        raw_reentry = risk_controls.get("riskOffReentry")
        if raw_reentry is not None:
            if not isinstance(raw_reentry, dict):
                errors.append("riskControls.riskOffReentry:must_be_object")
            else:
                risk_off_reentry = raw_reentry
                if not isinstance(raw_reentry.get("enabled"), bool):
                    errors.append("riskControls.riskOffReentry.enabled:required_boolean")
                _number(
                    raw_reentry.get("maxMonthlyReentryPct"),
                    "riskControls.riskOffReentry.maxMonthlyReentryPct",
                    errors,
                    minimum=0.1,
                    maximum=100,
                )
                minimum_positive = raw_reentry.get("minimumPositiveFactorCount")
                if (
                    isinstance(minimum_positive, bool)
                    or not isinstance(minimum_positive, int)
                    or not 1 <= minimum_positive <= 4
                ):
                    errors.append("riskControls.riskOffReentry.minimumPositiveFactorCount:must_be_integer_1_to_4")
                _number(
                    raw_reentry.get("minimumAiConfidence"),
                    "riskControls.riskOffReentry.minimumAiConfidence",
                    errors,
                    minimum=0,
                    maximum=1,
                )
                directions = raw_reentry.get("allowedAiDirections")
                if (
                    not isinstance(directions, list)
                    or not directions
                    or any(str(item) not in {"OVERWEIGHT", "NEUTRAL"} for item in directions)
                ):
                    errors.append("riskControls.riskOffReentry.allowedAiDirections:invalid")

    sleeves = policy.get("assetSleeves")
    sleeve_ids: set[str] = set()
    cash_count = 0
    target_sum = 0.0
    if not isinstance(sleeves, list) or not sleeves:
        errors.append("assetSleeves:at_least_one_required")
        sleeves = []
    for index, sleeve in enumerate(sleeves):
        if not isinstance(sleeve, dict):
            errors.append(f"assetSleeves[{index}]:must_be_object")
            continue
        sleeve_id = str(sleeve.get("id") or "").strip()
        if not sleeve_id or sleeve_id in sleeve_ids:
            errors.append(f"assetSleeves[{index}].id:missing_or_duplicate")
        sleeve_ids.add(sleeve_id)
        asset_class = str(sleeve.get("assetClass") or "")
        if asset_class == "CASH":
            cash_count += 1
        risk_level = _number(sleeve.get("riskLevel"), f"assetSleeves[{index}].riskLevel", errors, maximum=5)
        minimum = _number(sleeve.get("minWeightPct"), f"assetSleeves[{index}].minWeightPct", errors, maximum=100)
        target = _number(sleeve.get("targetWeightPct"), f"assetSleeves[{index}].targetWeightPct", errors, maximum=100)
        maximum = _number(sleeve.get("maxWeightPct"), f"assetSleeves[{index}].maxWeightPct", errors, maximum=100)
        tactical = _number(sleeve.get("tacticalBudgetPct"), f"assetSleeves[{index}].tacticalBudgetPct", errors, maximum=20)
        if not minimum <= target <= maximum:
            errors.append(f"assetSleeves[{index}]:weight_order_invalid")
        if tactical > max(target - minimum, maximum - target) + 1e-9:
            errors.append(f"assetSleeves[{index}].tacticalBudgetPct:exceeds_band")
        if risk_level > 0 and asset_class == "CASH":
            errors.append(f"assetSleeves[{index}].riskLevel:cash_must_be_zero")
        target_sum += target
        codes = sleeve.get("approvedFundCodes")
        if not isinstance(codes, list):
            errors.append(f"assetSleeves[{index}].approvedFundCodes:must_be_list")
        else:
            for code in codes:
                if not FUND_CODE_RE.fullmatch(str(code)):
                    errors.append(f"assetSleeves[{index}].approvedFundCodes:invalid_code")
    if cash_count != 1:
        errors.append("assetSleeves:exactly_one_cash_sleeve_required")
    if abs(target_sum - 100.0) > 0.01:
        errors.append("assetSleeves:target_weights_must_sum_to_100")

    mapping = policy.get("fundSleeveMap")
    if not isinstance(mapping, dict):
        errors.append("fundSleeveMap:must_be_object")
    else:
        for code, sleeve_id in mapping.items():
            if not FUND_CODE_RE.fullmatch(str(code)):
                errors.append("fundSleeveMap:invalid_fund_code")
            if str(sleeve_id) not in sleeve_ids:
                errors.append(f"fundSleeveMap.{code}:unknown_sleeve")

    limits = policy.get("portfolioLimits") if isinstance(policy.get("portfolioLimits"), dict) else {}
    for field in (
        "maxEquityWeightPct",
        "maxThemeWeightPct",
        "maxSingleFundWeightPct",
        "maxOneTradeWeightPct",
        "maxMonthlyTurnoverPct",
    ):
        _number(limits.get(field), f"portfolioLimits.{field}", errors, maximum=100)
    if risk_off_reentry is not None and (number := risk_off_reentry.get("maxMonthlyReentryPct")):
        try:
            if float(number) > float(limits.get("maxMonthlyTurnoverPct")):
                errors.append("riskControls.riskOffReentry.maxMonthlyReentryPct:must_not_exceed_monthly_turnover_limit")
        except (TypeError, ValueError):
            pass
    _number(limits.get("minTradeCny"), "portfolioLimits.minTradeCny", errors)
    _number(limits.get("amountStepCny"), "portfolioLimits.amountStepCny", errors, minimum=0.01)
    for limit_field in ("maxEquityWeightPct", "maxThemeWeightPct"):
        aggregate_minimum = sum(
            _number(sleeve.get("minWeightPct"), f"{limit_field}.aggregateMinimum", [])
            for sleeve in sleeves
            if isinstance(sleeve, dict) and _counts_toward_limit(sleeve, limit_field)
        )
        limit_value = _number(limits.get(limit_field), f"portfolioLimits.{limit_field}", [])
        if aggregate_minimum > limit_value + 1e-9:
            errors.append(f"portfolioLimits.{limit_field}:below_aggregate_sleeve_minimum")
    if isinstance(risk_controls, dict):
        one_trade_limit = _number(limits.get("maxOneTradeWeightPct"), "portfolioLimits.maxOneTradeWeightPct", [])
        reduction_steps = risk_controls.get("reductionStepPctByAdverseFactorCount")
        if isinstance(reduction_steps, dict):
            for factor_count, step in reduction_steps.items():
                step_value = _number(
                    step,
                    f"riskControls.reductionStepPctByAdverseFactorCount.{factor_count}",
                    [],
                )
                if step_value > one_trade_limit + 1e-9:
                    errors.append(
                        f"riskControls.reductionStepPctByAdverseFactorCount.{factor_count}:exceeds_one_trade_limit"
                    )

    preferences = policy.get("interactionPreferences") if isinstance(policy.get("interactionPreferences"), dict) else {}
    if preferences.get("adviceMode") != "DECISIVE":
        errors.append("interactionPreferences.adviceMode:must_be_DECISIVE")
    if preferences.get("requiresUserTradeDecision") is not True:
        errors.append("interactionPreferences.requiresUserTradeDecision:must_be_true")
    if status in CONFIRMED_STATUSES and policy.get("confirmedByUser") is not True:
        errors.append("confirmedByUser:must_be_true")
    return list(dict.fromkeys(errors))


def next_question(policy: dict[str, Any] | None) -> dict[str, str] | None:
    if not policy:
        return {
            "id": "goal_purpose_and_date",
            "question": "这笔钱最主要用来做什么，预计什么时候会用到？",
        }
    goals = policy.get("goals") if isinstance(policy.get("goals"), list) else []
    first_goal = goals[0] if goals and isinstance(goals[0], dict) else {}
    checks = [
        (not first_goal.get("purpose") or not first_goal.get("targetDate"), "goal_purpose_and_date", "这笔钱最主要用来做什么，预计什么时候会用到？"),
        (
            (
                first_goal.get("targetAmountCny") is None
                and first_goal.get("targetAmountMode") != "NONE"
            )
            or first_goal.get("plannedContributionCnyPerMonth") is None,
            "goal_amount_and_contribution",
            "目标金额、当前可投资金额，以及之后每月预计投入多少？",
        ),
        (not isinstance((policy.get("riskCapacity") or {}).get("emergencyFundReady"), bool), "liquidity_and_emergency", "投资账户之外是否已留足应急资金，未来12个月预计会取用多少？"),
        ((policy.get("riskCapacity") or {}).get("maxDrawdownPct") is None or (policy.get("riskTolerance") or {}).get("maxDrawdownPct") is None, "drawdown_limit", "这笔组合最多能接受多大阶段性亏损？我会同时换算成人民币压力金额给你确认。"),
        (not (policy.get("riskTolerance") or {}).get("stressReaction"), "stress_reaction", "达到这笔亏损时，你更可能补仓、继续持有，还是退出？"),
        (
            not isinstance(policy.get("drawdownBasis"), dict),
            "drawdown_basis",
            "回撤上限按全部可投资资产还是只按已买入基金计算？若按全部资产，是否接受在总资产净值历史补齐前使用可审计的静态现金代理口径？",
        ),
        (not policy.get("allowedAssets") or not isinstance(policy.get("excludedAssets"), list), "asset_permissions", "你允许和明确排除哪些资产：A股、港股/海外、债券、黄金、主动基金、主题基金？"),
        (not policy.get("assetSleeves") or not policy.get("portfolioLimits"), "allocation_and_limits", "请确认各资产目标区间，以及最大权益、主题、单基金和单笔交易上限。"),
        (not policy.get("interactionPreferences"), "interaction_preferences", "你希望多久收到一次常规建议和风险检查，是否启用策略快照归档？"),
    ]
    for missing, question_id, question in checks:
        if missing:
            return {"id": question_id, "question": question}
    return None


def _atomic_write(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temp_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=str(path.parent))
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            json.dump(value, handle, ensure_ascii=False, indent=2, sort_keys=True)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp_name, path)
    finally:
        if os.path.exists(temp_name):
            os.unlink(temp_name)


def persist(root: Path, key: str, policy: dict[str, Any], event_type: str, reason: str | None = None) -> dict[str, Any]:
    current_path, events_path, lock_path = user_paths(root, key)
    with locked(lock_path):
        errors = validate_policy(policy, allow_draft=policy.get("status") == "DRAFT")
        if errors:
            raise ValueError(";".join(errors))
        event = {
            "schemaVersion": "investor_policy_event.v1",
            "eventType": event_type,
            "occurredAt": utc_now(),
            "userKey": key,
            "policyVersion": policy["policyVersion"],
            "policyHash": content_hash(policy),
            "reason": reason,
            "policy": policy,
        }
        events_path.parent.mkdir(parents=True, exist_ok=True)
        with events_path.open("a", encoding="utf-8") as handle:
            handle.write(canonical_json(event) + "\n")
            handle.flush()
            os.fsync(handle.fileno())
        _atomic_write(current_path, policy)
    return event


def read_json(path: str) -> dict[str, Any]:
    value = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("input must contain a JSON object")
    return value


def prepare_version(input_policy: dict[str, Any], current: dict[str, Any] | None, status: str) -> dict[str, Any]:
    policy = deepcopy(input_policy)
    policy["schemaVersion"] = POLICY_SCHEMA
    policy["status"] = status
    policy["policyVersion"] = int((current or {}).get("policyVersion") or 0) + 1
    policy.pop("userId", None)
    policy.pop("uid", None)
    return policy


def status_payload(root: Path, key: str) -> dict[str, Any]:
    policy = load_current(root, key)
    return {
        "schemaVersion": "investor_policy_status.v1",
        "userKey": key,
        "state": policy.get("status") if policy else "ABSENT",
        "policy": policy,
        "nextQuestion": next_question(policy),
    }


def transition(root: Path, key: str, target: str, event_type: str, allowed: set[str], reason: str | None) -> dict[str, Any]:
    current = load_current(root, key)
    if not current:
        raise ValueError("no policy exists")
    if current.get("status") not in allowed:
        raise ValueError(f"invalid transition {current.get('status')} -> {target}")
    policy = deepcopy(current)
    policy["status"] = target
    policy["policyVersion"] = int(current["policyVersion"]) + 1
    if target in CONFIRMED_STATUSES:
        policy["confirmedByUser"] = True
    if target == "ACTIVE":
        policy["effectiveAt"] = utc_now()
    if target == "REVIEW_DUE":
        triggers = list(policy.get("reviewTriggers") or [])
        triggers.append({"at": utc_now(), "reason": reason or "unspecified"})
        policy["reviewTriggers"] = triggers
    persist(root, key, policy, event_type, reason)
    return status_payload(root, key)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--state-dir", default=None)
    subparsers = parser.add_subparsers(dest="command", required=True)
    for command in ("status", "shadow", "activate"):
        sub = subparsers.add_parser(command)
        sub.add_argument("--user-id", required=True)
    for command in ("save-draft", "confirm"):
        sub = subparsers.add_parser(command)
        sub.add_argument("--user-id", required=True)
        sub.add_argument("--input", required=True)
    for command in ("review-due", "suspend"):
        sub = subparsers.add_parser(command)
        sub.add_argument("--user-id", required=True)
        sub.add_argument("--reason", required=True)
    return parser


def main() -> None:
    args = build_parser().parse_args()
    root = Path(args.state_dir).expanduser().resolve() if args.state_dir else default_state_root()
    key = user_key(args.user_id)
    if args.command == "status":
        result = status_payload(root, key)
    elif args.command == "save-draft":
        current = load_current(root, key)
        policy = prepare_version(read_json(args.input), current, "DRAFT")
        persist(root, key, policy, "DRAFT_SAVED")
        result = status_payload(root, key)
    elif args.command == "confirm":
        current = load_current(root, key)
        policy = prepare_version(read_json(args.input), current, "CONFIRMED")
        policy["confirmedByUser"] = True
        policy["lastReviewedAt"] = utc_now()
        persist(root, key, policy, "POLICY_CONFIRMED")
        result = status_payload(root, key)
    elif args.command == "shadow":
        result = transition(root, key, "SHADOW", "SHADOW_STARTED", {"CONFIRMED"}, None)
    elif args.command == "activate":
        result = transition(root, key, "ACTIVE", "POLICY_ACTIVATED", {"SHADOW"}, None)
    elif args.command == "review-due":
        result = transition(root, key, "REVIEW_DUE", "REVIEW_REQUIRED", {"CONFIRMED", "SHADOW", "ACTIVE"}, args.reason)
    elif args.command == "suspend":
        result = transition(root, key, "SUSPENDED", "POLICY_SUSPENDED", CONFIRMED_STATUSES, args.reason)
    else:
        raise ValueError("unsupported command")
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
