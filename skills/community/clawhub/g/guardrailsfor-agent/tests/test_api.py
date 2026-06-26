from __future__ import annotations

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db import Base, get_db
from app.main import app


@pytest.fixture()
def client() -> TestClient:
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        future=True,
    )
    SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)
    Base.metadata.create_all(bind=engine)

    def override_get_db():
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


def test_create_policy_and_evaluate_deny(client: TestClient) -> None:
    policy = {
        "policy_id": "FIN-001",
        "name": "Block high transactions",
        "priority": 100,
        "policy_format": "structured",
        "definition": {
            "action_types": ["transaction.create"],
            "effect": "DENY",
            "conditions": [{"field": "payload.amount", "operator": "gt", "value": 1000}],
            "reason": "Transaction exceeds allowed limit",
        },
    }

    create_resp = client.post("/policies", json=policy)
    assert create_resp.status_code == 201

    evaluate_resp = client.post(
        "/evaluate",
        json={"action_id": "act-1", "action_type": "transaction.create", "payload": {"amount": 1500}},
    )
    assert evaluate_resp.status_code == 200
    body = evaluate_resp.json()
    assert body["result"]["decision"] == "DENY"
    assert body["result"]["policy_id"] == "FIN-001"


def test_natural_language_policy_parsing(client: TestClient) -> None:
    create_resp = client.post(
        "/policies",
        json={
            "policy_id": "FIN-010",
            "name": "Approval threshold",
            "policy_format": "natural_language",
            "raw_policy": "Require approval for transactions over $5000",
            "priority": 180,
        },
    )
    assert create_resp.status_code == 201

    evaluate_resp = client.post(
        "/evaluate",
        json={"action_type": "transaction.execute", "payload": {"amount": 5500}},
    )
    assert evaluate_resp.status_code == 200
    assert evaluate_resp.json()["result"]["decision"] == "REQUIRE_APPROVAL"


def test_yaml_policy_support(client: TestClient) -> None:
    yaml_policy = """
action_types: [message.send]
effect: DENY
conditions:
  - field: payload.contains_pii
    operator: eq
    value: true
reason: PII is blocked
"""

    create_resp = client.post(
        "/policies",
        json={
            "policy_id": "PRI-001",
            "name": "PII block",
            "policy_format": "yaml",
            "raw_policy": yaml_policy,
        },
    )
    assert create_resp.status_code == 201

    evaluate_resp = client.post(
        "/evaluate",
        json={"action_type": "message.send", "payload": {"contains_pii": True}},
    )
    assert evaluate_resp.status_code == 200
    assert evaluate_resp.json()["result"]["decision"] == "DENY"


def test_audit_records_written(client: TestClient) -> None:
    client.post(
        "/policies",
        json={
            "policy_id": "OPS-001",
            "name": "Require approval",
            "priority": 200,
            "policy_format": "structured",
            "definition": {
                "action_types": ["deploy.start"],
                "effect": "REQUIRE_APPROVAL",
                "conditions": [{"field": "payload.environment", "operator": "eq", "value": "prod"}],
                "reason": "Prod deployment requires approval",
                "requires_approval": True,
            },
        },
    )

    client.post("/evaluate", json={"action_type": "deploy.start", "payload": {"environment": "prod"}})

    audit_resp = client.get("/audit")
    assert audit_resp.status_code == 200
    entries = audit_resp.json()
    assert len(entries) == 1
    assert entries[0]["decision"]["decision"] == "REQUIRE_APPROVAL"


def test_seed_includes_git_and_email_guardrails(client: TestClient) -> None:
    seed_resp = client.post("/seed")
    assert seed_resp.status_code == 200

    eval_force_push = client.post(
        "/evaluate",
        json={"action_type": "git.push", "payload": {"force": True, "remote": "origin", "branch": "main"}},
    )
    assert eval_force_push.status_code == 200
    force_push_result = eval_force_push.json()["result"]
    assert force_push_result["decision"] == "DENY"
    assert force_push_result["policy_id"] == "OPS-GIT-001"

    eval_email_delete = client.post(
        "/evaluate",
        json={"action_type": "email.delete", "payload": {"folder": "inbox", "message_id": "abc-123"}},
    )
    assert eval_email_delete.status_code == 200
    email_delete_result = eval_email_delete.json()["result"]
    assert email_delete_result["decision"] == "REQUIRE_APPROVAL"
    assert email_delete_result["policy_id"] == "COM-EMAIL-001"
    assert email_delete_result["requires_approval"] is True


def test_seed_enforces_data_leak_guardrails(client: TestClient) -> None:
    seed_resp = client.post("/seed")
    assert seed_resp.status_code == 200

    deny_sensitive_external = client.post(
        "/evaluate",
        json={
            "action_type": "message.send",
            "payload": {"contains_sensitive_data": True, "is_external": True, "channel": "external_chat"},
        },
    )
    assert deny_sensitive_external.status_code == 200
    sensitive_result = deny_sensitive_external.json()["result"]
    assert sensitive_result["decision"] == "DENY"
    assert sensitive_result["policy_id"] == "DLP-001"

    deny_api_key = client.post(
        "/evaluate",
        json={
            "action_type": "response.generate",
            "payload": {"contains_api_key": True, "output_target": "customer_response"},
        },
    )
    assert deny_api_key.status_code == 200
    api_key_result = deny_api_key.json()["result"]
    assert api_key_result["decision"] == "DENY"
    assert api_key_result["policy_id"] == "DLP-002"

    deny_restricted_file = client.post(
        "/evaluate",
        json={"action_type": "file.read", "payload": {"is_restricted": True, "path": "/restricted/payroll.csv"}},
    )
    assert deny_restricted_file.status_code == 200
    restricted_file_result = deny_restricted_file.json()["result"]
    assert restricted_file_result["decision"] == "DENY"
    assert restricted_file_result["policy_id"] == "OPS-DATA-001"

    modify_personal_data = client.post(
        "/evaluate",
        json={
            "action_type": "response.generate",
            "payload": {"contains_personal_data": True, "text": "Contact Jane at +1-555-0101"},
        },
    )
    assert modify_personal_data.status_code == 200
    modify_result = modify_personal_data.json()["result"]
    assert modify_result["decision"] == "MODIFY"
    assert modify_result["policy_id"] == "COM-PII-001"
    assert modify_result["modifications"] == {"mask_personal_data": True}

    require_approval_external = client.post(
        "/evaluate",
        json={
            "action_type": "file.share",
            "payload": {"is_external": True, "contains_sensitive_data": False, "contains_personal_data": False},
        },
    )
    assert require_approval_external.status_code == 200
    approval_result = require_approval_external.json()["result"]
    assert approval_result["decision"] == "REQUIRE_APPROVAL"
    assert approval_result["policy_id"] == "COM-EXT-001"
    assert approval_result["requires_approval"] is True
