# JEP-Guard Audit Skill v1.0.0

**Strict JEP-04 / JAC-01 Compliant Audit Chain** with Friendly API Layer.

Based on:
- **JEP-04**: *Judgment Event Protocol* (draft-wang-jep-judgment-event-protocol-04)
- **JAC-01**: *Judgment Accountability Chain* (draft-wang-jac-01)

## Three-Layer Architecture

```
GuardSkill (API Layer)        — Friendly fields: issuer, assertion, target
        ↓
JEPAdapter (Mapping Layer)    — Maps friendly fields to strict JEP-04
        ↓
JEPCodec (Protocol Layer)     — Strict jep/verb/who/when/what/nonce/aud/ref/sig
```

## What It Does

| Feature | Description |
|---------|-------------|
| **Auto-Intercept** | Ingests FriendlyEvents; internally converts to strict JEP-04 |
| **Hash Chain** | SHA-256 linked audit chain with per-event integrity verification |
| **Nonce Enforcement** | UUIDv4 anti-replay per JEP-04 Section 2.3 |
| **Timestamp Window** | ±5 minute clock skew tolerance per JEP-04 |
| **JAC-01 Chain** | `task_based_on` parent judgment verification + fault extension support |
| **Violation Detection** | R001–R005 rules + protocol-level integrity checks |
| **Compliance Export** | EU AI Act / CA SB 1047 / CO SB 205 / Generic JEP-01 |

## Quick Start

```bash
pip install -r requirements.txt
uvicorn skill.api:app --host 0.0.0.0 --port 8000
```

## API

### Ingest

```bash
curl -X POST http://localhost:8000/audit/ingest   -H "Content-Type: application/json"   -d '{
    "session_id": "loan-001",
    "events": [
      {
        "event_id": "evt-1",
        "primitive": "J",
        "issuer": "did:example:agent-001",
        "timestamp": "2026-04-26T09:00:00Z",
        "target": "loan-decision",
        "assertion": {"subject": "app_123", "predicate": "approval", "value": "approved"},
        "confidence": 0.92,
        "signature": "sig..."
      }
    ]
  }'
```

### Chain Inspection

```bash
curl http://localhost:8000/audit/chain/loan-001
```

### Compliance Export

```bash
curl -X POST http://localhost:8000/audit/export   -H "Content-Type: application/json"   -d '{"session_id": "loan-001", "standard": "eu_ai_act"}'
```

## Violation Rules

| ID | Severity | Trigger |
|----|----------|---------|
| R001 | WARNING | Judge without subsequent Verify |
| R002 | VIOLATION | Delegate without prior J/V from same issuer |
| R003 | VIOLATION | Terminate referencing non-existent event |
| R004 | CRITICAL | Hash chain break (ref mismatch) |
| R005 | VIOLATION | Verify referencing non-existent Judge |

## Protocol Alignment

| JEP-04 Field | Guard API Field | Mapping |
|--------------|-----------------|---------|
| `jep` | (auto) | Fixed to "1" |
| `verb` | `primitive` | J/D/T/V |
| `who` | `issuer` | Actor DID |
| `when` | `timestamp` | ISO → Unix seconds |
| `what` | `assertion` | SHA-256 multihash of assertion |
| `nonce` | (auto) | UUIDv4 generated |
| `aud` | `target` | Intended recipient |
| `ref` | `prev_event_id` / `verify_of` | Chain link |
| `sig` | `signature` | JWS signature |
| `task_based_on` | `parent_task_hash` | JAC-01 causality |

## Example

```bash
cd examples
python strict_protocol_demo.py
```

---

Cognitive Emergence Lab  
yuqiang@humanjudgment.org
