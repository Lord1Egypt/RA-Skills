---
name: stamp
description: >
  Embeds a MO§ES™ governance stamp into every document produced this session.
  Active mode, posture, session ID, action sequence number, and SHA-256 integrity
  hash. The output itself is the audit record. Use when document provenance matters
  or outputs need to be traceable.
metadata:
  openclaw:
    emoji: 🔏
    tags: [stamp, provenance, audit, governed-output, document]
    version: 0.1.0
---

# MO§ES™ Governed Output — /stamp

When invoked, activate governed output for the remainder of this session.
Every document produced carries an embedded governance stamp — not as a
separate log, but inside the document itself. The output is the audit record.

## Activation

```
✓ Governed output active
Every document produced this session will be stamped with:
  — Active governance mode
  — Active posture
  — Session ID (SHA-256 of timestamp + first message, first 8 chars)
  — Action sequence number
  — Integrity hash (SHA-256 of content + governance state)
```

## Stamp Format

Append this block to the end of every qualifying document:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
MO§ES™ GOVERNANCE STAMP
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Produced under:  MO§ES™ Governance Framework
Mode:            [active mode, or Unrestricted if none set]
Posture:         [active posture, or None]
Role:            [active role, or Primary]
Session ID:      [first 8 chars of SHA-256(timestamp + first user message)]
Action #:        [sequential count of governed actions this session]
Integrity hash:  [SHA-256 of: document title + mode + posture + action #]
Lineage anchor:  5cda97fa (MOSES_ANCHOR — truncated)
Runtime:         OpenClaw / Claude Code
© 2026 Ello Cello LLC — MO§ES™ patent pending Serial No. 63/877,177
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## What Counts as a Document

**Stamp:**
- Reports, memos, plans, specs, briefs
- Emails drafted at the user's request
- Code files produced as a primary deliverable
- Any artifact intended for use outside the session

**Do NOT stamp:**
- Inline answers, clarifications, short explanations
- Intermediate reasoning steps
- Tool call outputs

## Deactivate

```
/stamp off
```

## Relationship to Audit Trail

The stamp embeds provenance in the document. The SHA-256 audit ledger
(`audit_stub.py`) records the governance event separately. Both are active
when governance is running — the stamp is the document-level proof, the
ledger is the session-level chain.
