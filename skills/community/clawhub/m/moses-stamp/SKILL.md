---
name: moses-stamp
description: "MO§ES™ Governed Output — embeds a governance stamp into every document produced. Mode, posture, session ID, and cryptographic integrity hash stamped on output. The document is the audit record. Part of the moses-governance bundle. Patent pending Serial No. 63/877,177."
metadata:
  openclaw:
    emoji: 🪙
    tags: [stamp, governed-output, audit, provenance, document-governance]
    version: 0.1.0
    bins:
      - python3
    stateDirs:
      - ~/.openclaw/governance
example: |
  # Generate a stamp
  python3 scripts/stamp.py generate --mode "High Security" --posture "DEFENSE" --role "Primary"
  # Append stamp to a document
  python3 scripts/stamp.py append --file report.md --mode "High Security" --posture "DEFENSE"
requires:
  - metadata.openclaw
---

# MO§ES™ Governed Output

When this skill is active, every document you produce carries an embedded governance stamp. The stamp is not a separate log — it lives inside the artifact. The document is the audit record.

**Enforcement is automatic.** You do not wait to be asked. After producing any qualifying document, append the stamp.

---

## Activation

When `moses-stamp` is installed and active, governed output is on by default. Confirm at session start:

```
✓ Governed output active
Every document produced this session will be stamped with:
  — Active governance mode
  — Active posture
  — Session ID
  — Action sequence number
  — Integrity hash (SHA-256 of content + governance state)
The output is the audit record.
```

---

## Stamp Tool

Call `stamp.py generate` to produce the stamp block, then append it to your output:

```bash
python3 scripts/stamp.py generate \
  --mode "$(python3 skills/moses-governance/scripts/init_state.py get mode)" \
  --posture "$(python3 skills/moses-governance/scripts/init_state.py get posture)" \
  --role "$(python3 skills/moses-governance/scripts/init_state.py get role)"
```

Or append directly to a file:

```bash
python3 scripts/stamp.py append --file <output_file.md>
```

---

## Stamp Format

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
MO§ES™ GOVERNANCE STAMP
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Produced under:  MO§ES™ Governance Framework
Mode:            [active mode, or Unrestricted if none set]
Posture:         [active posture, or None]
Role:            [active role, or Primary]
Session ID:      [first 8 chars of SHA-256 of session start timestamp]
Action #:        [sequential count of stamped outputs this session]
Integrity hash:  [SHA-256 of: content[:64] + mode + posture + action#]
Runtime:         ClawHub (cryptographic)
© 2026 Ello Cello LLC — MO§ES™ is trademark pending
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## What Counts as a Document

Stamp these:
- Reports, memos, plans, specs, briefs
- Emails drafted at user request
- Code files produced as a primary deliverable
- Any artifact intended for use outside this conversation

Do NOT stamp:
- Inline answers, clarifications, short explanations
- Intermediate reasoning steps
- Tool call outputs

---

## Relationship to the Audit Chain

The stamp is document-level provenance. The audit chain (`moses-audit`) is action-level provenance. Both can be active simultaneously — they record different things. When both are active, log the action first (`audit_stub.py log`), then append the stamp to the document.

---

## Deactivation

To deactivate for a session: set an environment variable or pass `--off` to the governing agent. The stamp is a default-on enforcement gate, not an optional feature.
