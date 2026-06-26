---
name: jep-primitive-skills
version: 1.0.0
description: JEP Primitive Skills — Atomic Reference Implementations of Judge, Delegate, Terminate, Verify for Agent Collaboration Grammar
author: Cognitive Emergence Lab <yuqiang@humanjudgment.org>
license: MIT
protocol: JEP
tags:
  - jep
  - primitive
  - judge
  - delegate
  - terminate
  - verify
  - atomic
  - grammar
entrypoint: skill.api:app
host_targets:
  - mcp
  - api
  - python
skills:
  - name: judge
    description: Initiate an observation assertion (J primitive)
    input_schema:
      type: object
      properties:
        issuer:
          type: string
        target:
          type: string
        subject:
          type: string
        predicate:
          type: string
        value: {}
        confidence:
          type: number
        parent_task_hash:
          type: string
        signature:
          type: string
      required: [issuer, target, subject, predicate, value]
    output_schema:
      type: object
      properties:
        success:
          type: boolean
        primitive:
          type: string
        nonce:
          type: string
        who:
          type: string
        when:
          type: integer
        what:
          type: string
        message:
          type: string
        next_suggested_primitive:
          type: string
        canonical_json:
          type: string
  - name: delegate
    description: Transfer authority to another agent (D primitive)
    input_schema:
      type: object
      properties:
        issuer:
          type: string
        delegate_to:
          type: string
        target:
          type: string
        scope:
          type: string
        prev_event_id:
          type: string
        signature:
          type: string
      required: [issuer, delegate_to, target]
    output_schema:
      type: object
      properties:
        success:
          type: boolean
        primitive:
          type: string
        nonce:
          type: string
        who:
          type: string
        when:
          type: integer
        what:
          type: string
        message:
          type: string
        next_suggested_primitive:
          type: string
        canonical_json:
          type: string
  - name: terminate
    description: Close the lifecycle of a prior assertion (T primitive)
    input_schema:
      type: object
      properties:
        issuer:
          type: string
        terminate_of:
          type: string
        target:
          type: string
        reason:
          type: string
        prev_event_id:
          type: string
        signature:
          type: string
      required: [issuer, terminate_of, target]
    output_schema:
      type: object
      properties:
        success:
          type: boolean
        primitive:
          type: string
        nonce:
          type: string
        who:
          type: string
        when:
          type: integer
        what:
          type: string
        message:
          type: string
        next_suggested_primitive:
          type: string
        canonical_json:
          type: string
  - name: verify
    description: Cross-validate an existing assertion (V primitive)
    input_schema:
      type: object
      properties:
        issuer:
          type: string
        verify_of:
          type: array
          items:
            type: string
        target:
          type: string
        verification_result:
          type: string
          enum: [confirmed, rejected, partial]
        confidence:
          type: number
        prev_event_id:
          type: string
        signature:
          type: string
      required: [issuer, verify_of, target]
    output_schema:
      type: object
      properties:
        success:
          type: boolean
        primitive:
          type: string
        nonce:
          type: string
        who:
          type: string
        when:
          type: integer
        what:
          type: string
        message:
          type: string
        next_suggested_primitive:
          type: string
        canonical_json:
          type: string
---

# JEP Primitive Skills

**Atomic Reference Implementations of Judge, Delegate, Terminate, Verify**

## The Four Primitives

| Primitive | Verb | Purpose |
|-----------|------|---------|
| **Judge** | J | Initiate an observation assertion |
| **Delegate** | D | Transfer authority to another agent |
| **Terminate** | T | Close the lifecycle of a prior assertion |
| **Verify** | V | Cross-validate an existing assertion |

## Complete Cognitive Interaction Algebra

These four primitives form a complete algebra:
- **J** creates state.
- **V** validates state.
- **D** distributes responsibility for state.
- **T** invalidates state.

Any complex multi-agent collaboration decomposes into ordered combinations of these four atoms. No fifth primitive is required.

## Protocol Alignment

All events produced are strict JEP-04 compliant:
- `jep`: "1"
- `verb`: J/D/T/V
- `who`: issuer DID
- `when`: Unix timestamp
- `what`: SHA-256 multihash of payload
- `nonce`: UUIDv4
- `aud`: target
- `ref`: chain link
- `sig`: JWS signature
- `task_based_on`: JAC-01 parent task hash

## Integration

Events feed directly into:
- **Determinability-Checker** — causal sufficiency verification
- **COE-Consensus** — shared world state formation
- **JEP-Guard-Audit** — compliance chain generation

---

Cognitive Emergence Lab  
yuqiang@humanjudgment.org
