# JEP Primitive Skills v1.0.0

**Atomic Reference Implementations of Judge, Delegate, Terminate, Verify**

Based on **JEP-04** (draft-wang-jep-judgment-event-protocol-04) and **JAC-01** (draft-wang-jac-01).

> **Core Principle:** Any complex multi-agent collaboration can be decomposed into an ordered combination of these four atomic operations. No fifth primitive is required.

## The Four Primitives

| Primitive | Verb | Purpose | When to Use |
|-----------|------|---------|-------------|
| **Judge** | J | Initiate an observation assertion | "I observe X at this time" |
| **Delegate** | D | Transfer authority to another agent | "I authorize you to observe/confirm X" |
| **Terminate** | T | Close the lifecycle of a prior assertion | "This observation is no longer valid" |
| **Verify** | V | Cross-validate an existing assertion | "I confirm/verify that observation" |

## Architecture

```
PrimitiveSkill (API Layer)    — Friendly execute() methods
        ↓
JEPAdapter (Mapping Layer)    — FriendlyEvent → JEP04Event
        ↓
JEPCodec (Protocol Layer)     — Strict jep/verb/who/when/what/nonce/aud/ref/sig
```

## Quick Start

```bash
pip install -r requirements.txt
uvicorn skill.api:app --host 0.0.0.0 --port 8000
```

## API

### Judge

```bash
curl -X POST http://localhost:8000/judge   -H "Content-Type: application/json"   -d '{
    "issuer": "did:example:robotA",
    "target": "warehouse-zone-3",
    "subject": "door_01",
    "predicate": "status",
    "value": "open",
    "confidence": 0.95
  }'
```

### Delegate

```bash
curl -X POST http://localhost:8000/delegate   -H "Content-Type: application/json"   -d '{
    "issuer": "did:example:robotA",
    "delegate_to": "did:example:robotB",
    "target": "warehouse-zone-3",
    "scope": "continuous_observation"
  }'
```

### Terminate

```bash
curl -X POST http://localhost:8000/terminate   -H "Content-Type: application/json"   -d '{
    "issuer": "did:example:robotA",
    "terminate_of": "<nonce-of-prior-J-event>",
    "target": "warehouse-zone-3",
    "reason": "state_changed"
  }'
```

### Verify

```bash
curl -X POST http://localhost:8000/verify   -H "Content-Type: application/json"   -d '{
    "issuer": "did:example:robotB",
    "verify_of": ["<nonce-of-J-event>"],
    "target": "warehouse-zone-3",
    "verification_result": "confirmed",
    "confidence": 0.9
  }'
```

## Why These Four?

These four primitives form a **complete cognitive interaction algebra**:

- **J** creates state.
- **V** validates state.
- **D** distributes responsibility for state.
- **T** invalidates state.

Any complex scenario — robot collaboration, AR/VR co-presence, distributed scientific consensus, cognitive economy transactions — decomposes into sequences of these four atoms.

## Example

```bash
cd examples
python complex_workflow.py
```

Demonstrates a 7-step warehouse door monitoring workflow using only J/D/T/V.

## Integration

Events produced by these primitives are strict JEP-04 compliant and can be directly consumed by:

- **Determinability-Checker** — causal sufficiency verification
- **COE-Consensus** — shared world state formation
- **JEP-Guard-Audit** — compliance chain generation

---

Cognitive Emergence Lab  
yuqiang@humanjudgment.org
