---
name: jep-guard-audit
version: 1.0.0
description: JEP-Guard Audit Skill — Strict JEP-04/JAC-01 Compliant Audit Chain with Friendly API Layer
author: Cognitive Emergence Lab <yuqiang@humanjudgment.org>
license: MIT
protocol: JEP
tags:
  - jep
  - jac
  - audit
  - compliance
  - ai-act
  - guard
  - accountability
entrypoint: skill.api:app
host_targets:
  - mcp
  - api
  - python
skills:
  - name: audit_ingest
    description: Ingest developer-friendly events; internally converts to strict JEP-04/JAC-01
    input_schema:
      type: object
      properties:
        session_id:
          type: string
        events:
          type: array
          items:
            type: object
            properties:
              event_id:
                type: string
              primitive:
                type: string
                enum: [J, D, T, V]
              issuer:
                type: string
              timestamp:
                type: string
              target:
                type: string
              assertion:
                type: object
              delegate_to:
                type: string
              terminate_of:
                type: string
              verify_of:
                type: array
                items:
                  type: string
              verification_result:
                type: string
              confidence:
                type: number
              prev_event_id:
                type: string
              parent_task_hash:
                type: string
              signature:
                type: string
      required: [session_id, events]
    output_schema:
      type: object
      properties:
        session_id:
          type: string
        events_ingested:
          type: integer
        status:
          type: string
  - name: audit_chain
    description: Retrieve strict JEP-04 audit chain with integrity verification
    input_schema:
      type: object
      properties:
        session_id:
          type: string
      required: [session_id]
    output_schema:
      type: object
      properties:
        session_id:
          type: string
        chain_valid:
          type: boolean
        total_events:
          type: integer
        violation_count:
          type: integer
        warning_count:
          type: integer
        links:
          type: array
          items:
            type: object
  - name: audit_export
    description: Export regulatory compliance report (eu_ai_act, us_california, us_colorado, generic)
    input_schema:
      type: object
      properties:
        session_id:
          type: string
        standard:
          type: string
          enum: [generic, eu_ai_act, us_california, us_colorado]
      required: [session_id, standard]
    output_schema:
      type: object
      properties:
        report_id:
          type: string
        standard:
          type: string
        chain_summary:
          type: object
        findings:
          type: array
        recommendations:
          type: array
        raw_data:
          type: string
---

# JEP-Guard Audit Skill

**Strict JEP-04 / JAC-01 Compliant Audit Chain**

## Architecture

Three-layer design:
1. **GuardSkill** — Friendly API (`issuer`, `assertion`, `target`)
2. **JEPAdapter** — Maps friendly fields to strict JEP-04
3. **JEPCodec** — Strict protocol implementation (`jep`, `verb`, `who`, `when`, `what`, `nonce`, `aud`, `ref`, `sig`)

## Protocol Alignment

| JEP-04 Field | API Field | Notes |
|--------------|-----------|-------|
| `jep` | (auto) | Fixed to "1" |
| `verb` | `primitive` | J/D/T/V |
| `who` | `issuer` | Actor DID |
| `when` | `timestamp` | ISO → Unix seconds |
| `what` | `assertion` | SHA-256 multihash |
| `nonce` | (auto) | UUIDv4 |
| `aud` | `target` | Recipient |
| `ref` | `prev_event_id` / `verify_of` | Chain link |
| `sig` | `signature` | JWS |
| `task_based_on` | `parent_task_hash` | JAC-01 causality |

## Compliance Standards

- **EU AI Act** — Article 12 record-keeping, 6-year retention
- **California SB 1047** — 72-hour critical incident reporting
- **Colorado SB 205** — Algorithmic impact assessment + appeal logs
- **Generic JEP-01** — Baseline accountability tracing

---

Cognitive Emergence Lab  
yuqiang@humanjudgment.org
