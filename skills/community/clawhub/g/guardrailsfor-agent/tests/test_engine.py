from __future__ import annotations

from datetime import datetime
from types import SimpleNamespace

from app.engine import evaluate_action
from app.schemas import ActionRequest, DecisionType


def _policy(policy_id: str, name: str, priority: int, definition: dict, enabled: bool = True):
    return SimpleNamespace(
        policy_id=policy_id,
        name=name,
        priority=priority,
        definition=definition,
        enabled=enabled,
    )


def test_denies_transaction_over_limit() -> None:
    policies = [
        _policy(
            "FIN-001",
            "Deny high transactions",
            100,
            {
                "action_types": ["transaction.create"],
                "effect": "DENY",
                "conditions": [{"field": "payload.amount", "operator": "gt", "value": 1000}],
                "reason": "Transaction exceeds limit",
            },
        )
    ]

    result = evaluate_action(
        ActionRequest(action_type="transaction.create", payload={"amount": 1500}),
        policies,
    )

    assert result.decision == DecisionType.DENY
    assert result.policy_id == "FIN-001"


def test_priority_wins_in_conflicting_effects() -> None:
    policies = [
        _policy(
            "FIN-001",
            "Deny over 1000",
            100,
            {
                "action_types": ["transaction.create"],
                "effect": "DENY",
                "conditions": [{"field": "payload.amount", "operator": "gt", "value": 1000}],
                "reason": "Too high",
            },
        ),
        _policy(
            "FIN-002",
            "Approval over 5000",
            200,
            {
                "action_types": ["transaction.create"],
                "effect": "REQUIRE_APPROVAL",
                "conditions": [{"field": "payload.amount", "operator": "gt", "value": 5000}],
                "reason": "Needs approval",
                "requires_approval": True,
            },
        ),
    ]

    result = evaluate_action(
        ActionRequest(action_type="transaction.create", payload={"amount": 6000}),
        policies,
    )

    assert result.decision == DecisionType.REQUIRE_APPROVAL
    assert result.policy_id == "FIN-002"
    assert result.requires_approval is True


def test_modify_returns_changes() -> None:
    policies = [
        _policy(
            "COM-001",
            "Redact outbound",
            100,
            {
                "action_types": ["message.send"],
                "effect": "MODIFY",
                "conditions": [
                    {"field": "payload.channel", "operator": "eq", "value": "external_chat"},
                    {"field": "payload.contains_internal_ticket_id", "operator": "eq", "value": True},
                ],
                "reason": "Must redact internal IDs",
                "modifications": {"redact_internal_ticket_ids": True},
            },
        )
    ]

    result = evaluate_action(
        ActionRequest(
            action_type="message.send",
            payload={"channel": "external_chat", "contains_internal_ticket_id": True},
        ),
        policies,
    )

    assert result.decision == DecisionType.MODIFY
    assert result.modifications == {"redact_internal_ticket_ids": True}


def test_time_outside_denies() -> None:
    policies = [
        _policy(
            "OPS-001",
            "Working hours only",
            100,
            {
                "action_types": ["infrastructure.change"],
                "effect": "DENY",
                "conditions": [
                    {
                        "field": "timestamp",
                        "operator": "time_outside",
                        "value": "08:00",
                        "value_to": "18:00",
                    }
                ],
                "reason": "Outside working hours",
            },
        )
    ]

    result = evaluate_action(
        ActionRequest(
            action_type="infrastructure.change",
            timestamp=datetime.fromisoformat("2026-02-23T22:15:00"),
            payload={},
        ),
        policies,
    )

    assert result.decision == DecisionType.DENY
    assert result.reason == "Outside working hours"
