# Agent Policy & Guardrails Engine

A production-oriented policy enforcement layer for autonomous agents.

This service evaluates proposed agent actions against a policy set and returns one of:

- `ALLOW`
- `DENY`
- `MODIFY`
- `REQUIRE_APPROVAL`

It is infrastructure, not an agent/chatbot.

## Stack

- Python 3.11+
- FastAPI
- SQLAlchemy
- SQLite (default) or Postgres via env var

## Features

- Policy input formats:
  - Structured JSON objects
  - YAML policies
  - Natural-language policies (supported templates)
- Policy domains supported:
  - Financial limits
  - Privacy restrictions
  - Operational constraints
  - Communication rules
  - Approval thresholds
  - Time-based rules
  - Tool-action safety rules (example: deny `git.push` when `payload.force=true`)
  - Destructive-action approval rules (example: require approval for `email.delete` in inbox)
  - Data-leak prevention defaults:
    - Deny sensitive data to external destinations (`payload.contains_sensitive_data=true`, `payload.is_external=true`)
    - Deny API key exposure (`payload.contains_api_key=true`)
    - Deny restricted file access (`payload.is_restricted=true`)
    - Mask personal data in outbound outputs (`payload.contains_personal_data=true`)
    - Require approval for external sharing (`payload.is_external=true`)
- Enforcement engine:
  - Action-type matching
  - Condition evaluation (numeric, equality, set-membership, time windows)
  - Priority-based conflict resolution
  - Machine-readable decisions + human-readable explanation
- Audit logging for every evaluation

## Conflict Resolution

When multiple policies match:

1. Highest `priority` wins.
2. If tied on priority, stricter effect wins using:
   - `DENY > REQUIRE_APPROVAL > MODIFY > ALLOW`

## Quick Start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Service runs on `http://127.0.0.1:8000`.

## Configuration

Environment variables use prefix `GUARDRAILS_`:

- `GUARDRAILS_DATABASE_URL`
  - Default: `sqlite:///./guardrails.db`
  - Postgres example: `postgresql+psycopg://user:pass@localhost:5432/guardrails`

## API

- `GET /health`
- `POST /policies`
- `GET /policies`
- `GET /policies/{policy_id}`
- `PATCH /policies/{policy_id}`
- `DELETE /policies/{policy_id}` (soft-disable)
- `POST /evaluate`
- `GET /audit`
- `POST /seed` (load baseline policies)

## Example: Structured Policy

```json
{
  "policy_id": "FIN-001",
  "name": "Max transaction without approval",
  "priority": 200,
  "policy_format": "structured",
  "definition": {
    "action_types": ["transaction.create", "transaction.execute"],
    "effect": "REQUIRE_APPROVAL",
    "conditions": [
      {"field": "payload.amount", "operator": "gt", "value": 5000}
    ],
    "reason": "Transaction exceeds approval threshold of 5000",
    "requires_approval": true
  }
}
```

## Example: Natural Language Policy

```json
{
  "policy_id": "FIN-002",
  "name": "Deny high spend",
  "priority": 250,
  "policy_format": "natural_language",
  "raw_policy": "Deny transactions over $10000"
}
```

## Example: Evaluate Action

```json
{
  "action_id": "act-123",
  "action_type": "transaction.execute",
  "timestamp": "2026-02-23T12:00:00Z",
  "actor_id": "agent-7",
  "payload": {
    "amount": 12000,
    "currency": "USD"
  },
  "context": {
    "workspace": "prod"
  }
}
```

Example response:

```json
{
  "action_id": "act-123",
  "action_type": "transaction.execute",
  "result": {
    "decision": "DENY",
    "reason": "Transaction exceeds allowed spending limit",
    "policy_id": "FIN-001",
    "requires_approval": false,
    "modifications": {},
    "matched_policies": [],
    "explanation": "Matched policies and resolved by priority/severity"
  }
}
```

## Run Tests

```bash
pytest
```

## Notes on Natural Language Policies

Natural-language parsing is deterministic/template-based for reliability. Supported examples include:

- `deny transactions over 1000`
- `require approval for transactions over 5000`
- `deny sending pii over email`
- `deny operations outside 08:00 and 18:00`

For complex controls, use structured JSON/YAML policies.
