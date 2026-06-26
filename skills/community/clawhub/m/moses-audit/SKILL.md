---
name: moses-audit
description: "MO§ES™ Audit Trail — SHA-256 chained append-only governance ledger. Every agent appends before final response. Provides moses_log_action and moses_verify_chain tools. Tamper-evident. Part of the moses-governance bundle. Patent pending Serial No. 63/877,177."
metadata:
  openclaw:
    emoji: 🔐
    tags: [audit, sha256, tamper-evident, governance, ledger]
    version: 0.1.2
    bins:
      - python3
    env:
      - MOSES_OPERATOR_SECRET
    stateDirs:
      - ~/.openclaw/audits/moses
      - ~/.openclaw/governance
example: |
  # Log an action
  python3 scripts/audit_stub.py log --agent primary --action "treasury_check" --detail "50 SOL transfer evaluated" --outcome "held_pending_confirmation"
  # Verify chain
  python3 scripts/audit_stub.py verify
---

# MO§ES™ Audit Trail

Every governed action is logged. Every log entry is hashed. Every hash references the previous. The chain is tamper-evident and append-only.

**You must log before your final response.** Skipping the audit is a constitutional violation. It will be caught by the Observer and flagged.

---

## moses_log_action Tool

Call this before every final response:

```
<tool name="moses_log_action">
  <agent>primary|secondary|observer</agent>
  <action>short description of what was done</action>
  <detail>specifics — what was evaluated, what was blocked, what was executed</detail>
  <outcome>result: executed | blocked | held | flagged | logged</outcome>
</tool>
```

Or via script:
```bash
python3 ~/.openclaw/workspace/skills/moses-governance/scripts/audit_stub.py log \
  --agent primary \
  --action "treasury_transfer_check" \
  --detail "Transfer 50 SOL to 7xK...3nR evaluated under High Security + DEFENSE" \
  --outcome "held_pending_confirmation"
```

---

## moses_verify_chain Tool

Call when operator runs `/audit verify`:

```
<tool name="moses_verify_chain" />
```

Or via script:
```bash
python3 ~/.openclaw/workspace/skills/moses-governance/scripts/audit_stub.py verify
```

Returns: `[VERIFY OK] Chain intact. N entries verified.`
Or: `[VERIFY FAILED] Entry N: hash mismatch. Chain broken.`

---

## /audit Command Handler

| Command | Action |
|---------|--------|
| `/audit recent` | `python3 audit_stub.py recent --n 10` |
| `/audit verify` | `python3 audit_stub.py verify` |
| `/audit recent 25` | `python3 audit_stub.py recent --n 25` |

---

## Ledger Format

File: `~/.openclaw/audits/moses/audit_ledger.jsonl`

Each line is a JSON entry:
```json
{
  "timestamp": "2026-03-13T14:22:01Z",
  "agent": "primary",
  "component": "moses-audit",
  "action": "treasury_transfer_check",
  "detail": "Transfer 50 SOL — held by DEFENSE posture",
  "outcome": "held_pending_confirmation",
  "mode": "high-security",
  "posture": "defense",
  "role": "primary",
  "previous_hash": "abc123...",
  "hash": "def456..."
}
```

---

## Audit Mandate

Every agent in the MO§ES™ hierarchy appends to this shared ledger before final response. The ledger is:
- **Append-only** — nothing deleted, nothing modified
- **Hash-chained** — every entry references previous entry's hash
- **Governance-aware** — active mode/posture/role recorded with every entry
- **Verifiable** — full chain can be verified at any time

Session hashes (① config + ② content) are derived from the ledger. Onchain anchoring (③ — planned, not yet implemented) will write the chain tip to Solana or Base as a memo transaction.

---

## Data Sensitivity

The `detail` field is freeform. Do not log raw secrets, private keys, tokens, or PII in this field. Log action descriptions and outcomes only. Example of what belongs:

```
detail: "Transfer 50 SOL evaluated under High Security + DEFENSE — held pending confirmation"
```

Not:

```
detail: "API key sk-abc123 used to authenticate transfer"
```

`MOSES_OPERATOR_SECRET` is used locally for HMAC attestation only. It is never written to the ledger and never transmitted.
