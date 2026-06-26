from __future__ import annotations

import json
import re
from typing import Any

import yaml
from pydantic import ValidationError

from app.schemas import DecisionType, StructuredPolicyDefinition


def parse_structured_definition(raw: dict[str, Any]) -> dict[str, Any]:
    try:
        return StructuredPolicyDefinition.model_validate(raw).model_dump()
    except ValidationError as exc:
        raise ValueError(f"Invalid policy definition: {exc}") from exc


def parse_json_policy(raw_policy: str) -> dict[str, Any]:
    try:
        loaded = json.loads(raw_policy)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON policy: {exc}") from exc
    return parse_structured_definition(loaded)


def parse_yaml_policy(raw_policy: str) -> dict[str, Any]:
    try:
        loaded = yaml.safe_load(raw_policy)
    except yaml.YAMLError as exc:
        raise ValueError(f"Invalid YAML policy: {exc}") from exc
    if not isinstance(loaded, dict):
        raise ValueError("YAML policy must produce an object/dictionary")
    return parse_structured_definition(loaded)


def parse_natural_language_policy(raw_policy: str) -> dict[str, Any]:
    text = " ".join(raw_policy.strip().split()).lower()

    amount_patterns = [
        (
            r"deny\s+transactions?\s+over\s+\$?(?P<amount>[0-9]+(?:\.[0-9]{1,2})?)",
            DecisionType.DENY,
            "Transaction exceeds allowed spending limit",
            False,
        ),
        (
            r"require\s+approval\s+for\s+transactions?\s+over\s+\$?(?P<amount>[0-9]+(?:\.[0-9]{1,2})?)",
            DecisionType.REQUIRE_APPROVAL,
            "Transaction requires approval due to spending threshold",
            True,
        ),
    ]

    for pattern, effect, reason, requires_approval in amount_patterns:
        match = re.search(pattern, text)
        if match:
            amount = float(match.group("amount"))
            definition = StructuredPolicyDefinition(
                action_types=["transaction.create", "transaction.execute"] if "transactions" in text else ["*"],
                effect=effect,
                conditions=[
                    {
                        "field": "payload.amount",
                        "operator": "gt",
                        "value": amount,
                    }
                ],
                reason=reason,
                requires_approval=requires_approval,
            )
            return definition.model_dump()

    pii_match = re.search(r"deny\s+(sharing|sending)\s+(pii|sensitive\s+data).*(email|slack|sms)", text)
    if pii_match:
        channel = pii_match.group(3)
        definition = StructuredPolicyDefinition(
            action_types=["message.send", "email.send", "notification.send", "*"],
            effect=DecisionType.DENY,
            conditions=[
                {"field": "payload.contains_pii", "operator": "eq", "value": True},
                {"field": "payload.channel", "operator": "eq", "value": channel},
            ],
            reason="Privacy policy blocks transmission of PII on restricted channels",
        )
        return definition.model_dump()

    time_match = re.search(
        r"(allow|deny)\s+.*\s+(between|outside)\s+(?P<start>\d{1,2}:\d{2})\s+(and|to|-)\s+(?P<end>\d{1,2}:\d{2})",
        text,
    )
    if time_match:
        mode = time_match.group(1)
        boundary = time_match.group(2)
        start = time_match.group("start")
        end = time_match.group("end")
        operator = "time_outside" if boundary == "outside" else "time_between"
        effect = DecisionType.DENY if mode == "deny" else DecisionType.ALLOW
        definition = StructuredPolicyDefinition(
            action_types=["*"],
            effect=effect,
            conditions=[
                {
                    "field": "timestamp",
                    "operator": operator,
                    "value": start,
                    "value_to": end,
                    "timezone": "UTC",
                }
            ],
            reason="Action violates allowed operating time window",
        )
        return definition.model_dump()

    raise ValueError(
        "Could not parse natural language policy. Use a structured policy, or use a supported template "
        "(e.g. 'deny transactions over 1000', 'require approval for transactions over 5000')."
    )
