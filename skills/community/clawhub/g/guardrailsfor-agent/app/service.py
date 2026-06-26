from __future__ import annotations

from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.engine import evaluate_action
from app.models import AuditLog, Policy
from app.policy_parser import (
    parse_json_policy,
    parse_natural_language_policy,
    parse_structured_definition,
    parse_yaml_policy,
)
from app.schemas import ActionRequest, DecisionResponse, PolicyCreate, PolicyFormat, PolicyUpdate


def _compile_policy(create: PolicyCreate) -> dict:
    if create.policy_format == PolicyFormat.STRUCTURED:
        definition = create.definition
        if hasattr(definition, "model_dump"):
            return definition.model_dump()  # type: ignore[no-any-return]
        return parse_structured_definition(definition or {})
    if create.policy_format == PolicyFormat.JSON:
        return parse_json_policy(create.raw_policy or "")
    if create.policy_format == PolicyFormat.YAML:
        return parse_yaml_policy(create.raw_policy or "")
    if create.policy_format == PolicyFormat.NATURAL_LANGUAGE:
        return parse_natural_language_policy(create.raw_policy or "")
    raise ValueError(f"Unsupported policy format: {create.policy_format}")


def create_policy(db: Session, payload: PolicyCreate) -> Policy:
    existing = db.execute(select(Policy).where(Policy.policy_id == payload.policy_id)).scalar_one_or_none()
    if existing:
        raise ValueError(f"Policy '{payload.policy_id}' already exists")

    compiled = _compile_policy(payload)
    policy = Policy(
        policy_id=payload.policy_id,
        name=payload.name,
        description=payload.description,
        policy_format=payload.policy_format.value,
        source_text=payload.raw_policy,
        definition=compiled,
        priority=payload.priority,
        enabled=payload.enabled,
    )
    db.add(policy)
    db.commit()
    db.refresh(policy)
    return policy


def list_policies(db: Session) -> list[Policy]:
    return list(db.execute(select(Policy).order_by(Policy.priority.desc(), Policy.policy_id)).scalars().all())


def get_policy(db: Session, policy_id: str) -> Optional[Policy]:
    return db.execute(select(Policy).where(Policy.policy_id == policy_id)).scalar_one_or_none()


def update_policy(db: Session, policy: Policy, payload: PolicyUpdate) -> Policy:
    updates = payload.model_dump(exclude_unset=True)
    if "definition" in updates:
        definition = updates["definition"]
        if hasattr(definition, "model_dump"):
            policy.definition = definition.model_dump()
        else:
            policy.definition = parse_structured_definition(definition)

    for field in ("name", "description", "priority", "enabled"):
        if field in updates:
            setattr(policy, field, updates[field])

    db.add(policy)
    db.commit()
    db.refresh(policy)
    return policy


def evaluate(db: Session, action: ActionRequest) -> DecisionResponse:
    policies = list(db.execute(select(Policy).where(Policy.enabled.is_(True))).scalars().all())
    result = evaluate_action(action, policies)

    audit = AuditLog(
        action_id=action.action_id,
        action_type=action.action_type,
        action_payload=action.model_dump(mode="json"),
        decision=result.model_dump(mode="json"),
        matched_policies=[p.model_dump(mode="json") for p in result.matched_policies],
    )
    db.add(audit)
    db.commit()

    return result


def list_audit_logs(db: Session, limit: int = 50) -> list[AuditLog]:
    return list(
        db.execute(select(AuditLog).order_by(AuditLog.created_at.desc()).limit(limit)).scalars().all()
    )
