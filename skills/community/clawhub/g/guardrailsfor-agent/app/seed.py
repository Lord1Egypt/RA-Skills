from __future__ import annotations

from app.schemas import PolicyCreate


def default_policies() -> list[PolicyCreate]:
    return [
        PolicyCreate(
            policy_id="FIN-001",
            name="Max transaction without approval",
            description="Require approval above $5,000.",
            priority=200,
            policy_format="structured",
            definition={
                "action_types": ["transaction.create", "transaction.execute"],
                "effect": "REQUIRE_APPROVAL",
                "conditions": [{"field": "payload.amount", "operator": "gt", "value": 5000}],
                "reason": "Transaction exceeds approval threshold of 5000",
                "requires_approval": True,
            },
        ),
        PolicyCreate(
            policy_id="PRI-001",
            name="Restrict PII over email",
            description="No PII over external email channels.",
            priority=300,
            policy_format="structured",
            definition={
                "action_types": ["email.send", "message.send"],
                "effect": "DENY",
                "conditions": [
                    {"field": "payload.contains_pii", "operator": "eq", "value": True},
                    {"field": "payload.channel", "operator": "eq", "value": "email"},
                ],
                "reason": "PII cannot be sent over email",
            },
        ),
        PolicyCreate(
            policy_id="OPS-001",
            name="Maintenance window lock",
            description="Deny infra operations outside 08:00-18:00 UTC.",
            priority=250,
            policy_format="structured",
            definition={
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
                "reason": "Infrastructure changes are only allowed between 08:00-18:00 UTC",
            },
        ),
        PolicyCreate(
            policy_id="COM-001",
            name="Mask internal ticket IDs in outbound chat",
            description="Rewrite outbound messages to remove ticket IDs.",
            priority=100,
            policy_format="structured",
            definition={
                "action_types": ["message.send"],
                "effect": "MODIFY",
                "conditions": [
                    {"field": "payload.channel", "operator": "eq", "value": "external_chat"},
                    {"field": "payload.contains_internal_ticket_id", "operator": "eq", "value": True},
                ],
                "reason": "Outbound chat must redact internal ticket IDs",
                "modifications": {"redact_internal_ticket_ids": True},
            },
        ),
        PolicyCreate(
            policy_id="OPS-GIT-001",
            name="Block force pushes",
            description="Disallow git push --force operations.",
            priority=1000,
            policy_format="structured",
            definition={
                "action_types": ["git.push"],
                "effect": "DENY",
                "conditions": [{"field": "payload.force", "operator": "eq", "value": True}],
                "reason": "Force push is prohibited by repository protection policy",
            },
        ),
        PolicyCreate(
            policy_id="COM-EMAIL-001",
            name="Approval required for inbox deletion",
            description="Require explicit approval before deleting inbox emails.",
            priority=900,
            policy_format="structured",
            definition={
                "action_types": ["email.delete"],
                "effect": "REQUIRE_APPROVAL",
                "conditions": [{"field": "payload.folder", "operator": "eq", "value": "inbox"}],
                "reason": "Deleting inbox emails requires explicit approval",
                "requires_approval": True,
            },
        ),
        PolicyCreate(
            policy_id="DLP-001",
            name="Block sensitive data sharing to external destinations",
            description="Never send sensitive data to external destinations.",
            priority=960,
            policy_format="structured",
            definition={
                "action_types": ["email.send", "message.send", "file.share", "http.request", "webhook.send"],
                "effect": "DENY",
                "conditions": [
                    {"field": "payload.contains_sensitive_data", "operator": "eq", "value": True},
                    {"field": "payload.is_external", "operator": "eq", "value": True},
                ],
                "reason": "Sensitive data cannot be shared externally",
            },
        ),
        PolicyCreate(
            policy_id="DLP-002",
            name="Block API key exposure",
            description="Never expose API keys in outbound messages or shares.",
            priority=980,
            policy_format="structured",
            definition={
                "action_types": ["response.generate", "email.send", "message.send", "file.share", "http.request"],
                "effect": "DENY",
                "conditions": [{"field": "payload.contains_api_key", "operator": "eq", "value": True}],
                "reason": "API keys must never be exposed",
            },
        ),
        PolicyCreate(
            policy_id="OPS-DATA-001",
            name="Deny access to restricted files",
            description="Never allow reads/writes/deletes on restricted files without explicit bypass policy.",
            priority=990,
            policy_format="structured",
            definition={
                "action_types": ["file.read", "file.write", "file.delete", "file.download", "file.upload"],
                "effect": "DENY",
                "conditions": [{"field": "payload.is_restricted", "operator": "eq", "value": True}],
                "reason": "Access to restricted files is prohibited",
            },
        ),
        PolicyCreate(
            policy_id="COM-PII-001",
            name="Mask personal data in outbound outputs",
            description="Apply masking before personal data leaves the system.",
            priority=700,
            policy_format="structured",
            definition={
                "action_types": ["response.generate", "message.send", "email.send", "file.share"],
                "effect": "MODIFY",
                "conditions": [{"field": "payload.contains_personal_data", "operator": "eq", "value": True}],
                "reason": "Personal data must be masked in outbound outputs",
                "modifications": {"mask_personal_data": True},
            },
        ),
        PolicyCreate(
            policy_id="COM-EXT-001",
            name="Approval required for external sharing",
            description="Require explicit approval for external sharing actions.",
            priority=850,
            policy_format="structured",
            definition={
                "action_types": ["email.send", "message.send", "file.share", "http.request", "webhook.send"],
                "effect": "REQUIRE_APPROVAL",
                "conditions": [{"field": "payload.is_external", "operator": "eq", "value": True}],
                "reason": "External sharing requires explicit approval",
                "requires_approval": True,
            },
        ),
    ]
