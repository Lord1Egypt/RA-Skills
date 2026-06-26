# MO§ES™ Governance — OpenClaw Skill

Constitutional governance for AI agents. Role hierarchy, behavioral modes, posture controls, and SHA-256 chained audit trail.

**Patent pending:** Serial No. 63/877,177
**DOI:** https://zenodo.org/records/18792459
**Live demo:** https://mos2es.io

---

## Install

```bash
clawhub install moses-governance
```

Or manually:
```bash
cp -r skills/moses-governance ~/.openclaw/workspace/skills/
export MOSES_OPERATOR_SECRET='your-hmac-key'
python3 ~/.openclaw/workspace/skills/moses-governance/scripts/init_state.py init
```

## Quick Start

```bash
# Set governance mode
/govern high-security

# Set posture
/posture defense

# Set role
/role primary

# Check status
/status

# View audit trail
/audit recent
```

## What It Does

Every agent action is:
1. **Checked** against the active governance mode's constraints
2. **Filtered** through the active posture (SCOUT / DEFENSE / OFFENSE)
3. **Ordered** by role (Primary → Secondary → Observer)
4. **Logged** with SHA-256 hash to an append-only audit ledger

## Skill Family (Multi-Agent Bundle)

For multi-agent deployments, install the full bundle:
- `moses-roles` — Agent definitions + sequence enforcement
- `moses-modes` — Mode constraint injection
- `moses-postures` — Transaction + execution policy
- `moses-audit` — Shared SHA-256 ledger
- `moses-coordinator` — Optional daemon for sequence monitoring

## Files

```
moses-governance/
  SKILL.md                  ← Core governance skill
  README.md                 ← This file
  AMENDMENT-FORMAT.md       ← Constitutional amendment schema
  scripts/
    audit_stub.py           ← SHA-256 chained ledger
    init_state.py           ← Governance state manager
  references/
    modes.md                ← 8 governance mode definitions
    postures.md             ← SCOUT/DEFENSE/OFFENSE specs
    roles.md                ← Primary/Secondary/Observer specs
```

## © 2026 Ello Cello LLC
contact@burnmydays.com | https://mos2es.io
