from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Optional

from dateutil import parser as date_parser

from app.models import Policy
from app.schemas import ActionRequest, DecisionResponse, DecisionType, MatchedPolicy

SEVERITY_ORDER = {
    DecisionType.DENY: 4,
    DecisionType.REQUIRE_APPROVAL: 3,
    DecisionType.MODIFY: 2,
    DecisionType.ALLOW: 1,
}


def _value_by_path(data: Dict[str, Any], path: str) -> Any:
    current: Any = data
    for part in path.split("."):
        if not isinstance(current, dict) or part not in current:
            return None
        current = current[part]
    return current


def _as_datetime(value: Any) -> Optional[datetime]:
    if value is None:
        return None
    if isinstance(value, datetime):
        return value
    if isinstance(value, str):
        try:
            return date_parser.isoparse(value)
        except ValueError:
            return None
    return None


def _normalize_action(action: ActionRequest) -> Dict[str, Any]:
    return {
        "action_id": action.action_id,
        "action_type": action.action_type,
        "actor_id": action.actor_id,
        "timestamp": action.timestamp.isoformat() if action.timestamp else datetime.utcnow().isoformat(),
        "payload": action.payload,
        "context": action.context,
    }


def _time_in_range(target: str, start: str, end: str) -> bool:
    try:
        target_h, target_m = map(int, target.split(":"))
        start_h, start_m = map(int, start.split(":"))
        end_h, end_m = map(int, end.split(":"))
    except ValueError:
        return False

    target_total = target_h * 60 + target_m
    start_total = start_h * 60 + start_m
    end_total = end_h * 60 + end_m

    if start_total <= end_total:
        return start_total <= target_total <= end_total
    return target_total >= start_total or target_total <= end_total


def _evaluate_condition(action_data: Dict[str, Any], condition: Dict[str, Any]) -> bool:
    operator = condition.get("operator")
    actual = _value_by_path(action_data, condition.get("field", ""))
    expected = condition.get("value")
    expected_to = condition.get("value_to")

    if operator == "exists":
        return actual is not None
    if operator == "eq":
        return actual == expected
    if operator == "neq":
        return actual != expected
    if operator == "gt":
        return actual is not None and actual > expected
    if operator == "gte":
        return actual is not None and actual >= expected
    if operator == "lt":
        return actual is not None and actual < expected
    if operator == "lte":
        return actual is not None and actual <= expected
    if operator == "in":
        return actual in (expected or [])
    if operator == "not_in":
        return actual not in (expected or [])
    if operator == "contains":
        return actual is not None and expected in actual
    if operator == "between":
        return actual is not None and expected <= actual <= expected_to
    if operator in ("time_between", "time_outside"):
        dt = _as_datetime(actual) or _as_datetime(action_data.get("timestamp"))
        if dt is None:
            return False
        in_range = _time_in_range(dt.strftime("%H:%M"), str(expected), str(expected_to))
        return in_range if operator == "time_between" else (not in_range)

    return False


def _policy_applies_to_action(action_type: str, policy_action_types: List[str]) -> bool:
    if "*" in policy_action_types:
        return True
    return action_type in policy_action_types


def _matches_policy(action_data: Dict[str, Any], definition: Dict[str, Any]) -> bool:
    action_types = definition.get("action_types", ["*"])
    if not _policy_applies_to_action(action_data.get("action_type", ""), action_types):
        return False

    conditions = definition.get("conditions", [])
    return all(_evaluate_condition(action_data, condition) for condition in conditions)


def _merge_modifications(matched: List[MatchedPolicy]) -> Dict[str, Any]:
    merged: Dict[str, Any] = {}
    # Higher priority policies apply first and own conflicting keys.
    for mp in sorted(matched, key=lambda x: x.priority, reverse=True):
        if mp.effect != DecisionType.MODIFY:
            continue
        for key, value in mp.modifications.items():
            merged.setdefault(key, value)
    return merged


def _resolve_decision(matched: List[MatchedPolicy]) -> DecisionResponse:
    if not matched:
        return DecisionResponse(
            decision=DecisionType.ALLOW,
            reason="No active policy restrictions matched this action.",
            requires_approval=False,
            explanation="Action allowed by default because no policy conditions were triggered.",
            matched_policies=[],
        )

    sorted_by_priority = sorted(matched, key=lambda x: x.priority, reverse=True)
    top_priority = sorted_by_priority[0].priority
    same_priority = [mp for mp in sorted_by_priority if mp.priority == top_priority]
    winner = sorted(same_priority, key=lambda x: SEVERITY_ORDER[x.effect], reverse=True)[0]

    modifications = _merge_modifications(sorted_by_priority)
    requires_approval = winner.effect == DecisionType.REQUIRE_APPROVAL or winner.requires_approval

    effect_set = ", ".join(sorted({mp.effect.value for mp in same_priority}))
    explanation = (
        f"Matched {len(matched)} policy/policies. Conflict resolution used priority first, then effect severity "
        f"(DENY > REQUIRE_APPROVAL > MODIFY > ALLOW). Top priority={top_priority}; effects at this priority: {effect_set}."
    )

    return DecisionResponse(
        decision=winner.effect,
        reason=winner.reason,
        policy_id=winner.policy_id,
        requires_approval=requires_approval,
        modifications=modifications if winner.effect == DecisionType.MODIFY else {},
        matched_policies=sorted_by_priority,
        explanation=explanation,
    )


def evaluate_action(action: ActionRequest, policies: List[Policy]) -> DecisionResponse:
    action_data = _normalize_action(action)
    matched: List[MatchedPolicy] = []

    for policy in policies:
        if not policy.enabled:
            continue
        definition = policy.definition or {}
        if not _matches_policy(action_data, definition):
            continue

        matched.append(
            MatchedPolicy(
                policy_id=policy.policy_id,
                name=policy.name,
                priority=policy.priority,
                effect=DecisionType(definition.get("effect")),
                reason=definition.get("reason", f"Policy {policy.policy_id} matched"),
                modifications=definition.get("modifications", {}),
                requires_approval=bool(definition.get("requires_approval", False)),
            )
        )

    return _resolve_decision(matched)
