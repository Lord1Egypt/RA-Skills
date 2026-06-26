---
name: agent-policy-guardrails-engine
description: Build, run, and extend the Agent Policy & Guardrails Engine. Use when implementing policy formats, enforcement logic, decision conflict resolution, policy APIs, and audit/compliance workflows.
---

# Agent Policy & Guardrails Engine

## Use This Skill When

- You need to add or change policy enforcement behavior.
- You need to add policy types (financial, privacy, communication, operational, approval, time-based).
- You need to extend decision outputs (`ALLOW`, `DENY`, `MODIFY`, `REQUIRE_APPROVAL`).
- You need to update APIs, persistence, or audit logging.

## Project Layout

- `app/main.py`: FastAPI endpoints.
- `app/service.py`: orchestration for policy CRUD + evaluation + audit writes.
- `app/engine.py`: core policy evaluation and conflict resolution.
- `app/policy_parser.py`: JSON/YAML/NL policy parsing into structured definitions.
- `app/schemas.py`: request/response and policy schemas.
- `app/models.py`: SQLAlchemy models (`policies`, `audit_logs`).
- `app/seed.py`: baseline policies.
- `tests/test_api.py`: API-level behavior.
- `tests/test_engine.py`: decision logic behavior.

## Standard Workflow

1. Implement schema/model changes first if policy structure changes.
2. Update parser and engine evaluation paths.
3. Update API/service layer only as needed.
4. Add or update tests for both engine and API.
5. Run tests before finalizing.

## Commands

Install and test:

```bash
python3 -m pip install -r requirements.txt
python3 -m pytest
```

Run locally:

```bash
python3 -m uvicorn app.main:app --reload
```

## Enforcement Contract

All external agent/tool actions must be sent to `POST /evaluate` before execution.

Runtime handling expectations:

- `DENY`: block execution.
- `REQUIRE_APPROVAL`: pause and require explicit human approval.
- `MODIFY`: apply returned `modifications`, then execute.
- `ALLOW`: execute.

## Conflict Resolution Rules

When multiple policies match the same action:

1. Highest `priority` wins.
2. If tied on priority, effect severity wins:
   `DENY > REQUIRE_APPROVAL > MODIFY > ALLOW`.

## Adding New Guardrails

1. Add a structured policy in `app/seed.py` (optional baseline).
2. Ensure `action_types` and `conditions` map to real runtime payload fields.
3. Add API test coverage in `tests/test_api.py` using `/evaluate`.
4. Add engine-level tests in `tests/test_engine.py` for edge/conflict cases.

## Notes

- Keep policy evaluation deterministic.
- Prefer structured JSON/YAML policies for complex controls.
- Natural-language rules should compile into the same structured policy schema.
