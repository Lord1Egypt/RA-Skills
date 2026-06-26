---
name: moses-postures
description: "MO§ES™ Posture Controls — Enforces transaction and execution policies across all agents. SCOUT=read-only, DEFENSE=protect+confirm, OFFENSE=execute within mode. The throttle on top of governance modes. Part of the moses-governance bundle. Patent pending Serial No. 63/877,177."
metadata:
  openclaw:
    emoji: 🛡️
    tags: [governance, postures, transactions, safety]
    stateDirs:
      - ~/.openclaw/governance
    requires:
      - moses-governance
example: |
  # Set posture via operator command: /posture defense
  # Or directly: python3 ~/.openclaw/workspace/skills/moses-governance/scripts/init_state.py set --posture defense
---

# MO§ES™ Posture Controls

Posture is the throttle. Mode is the rulebook. Both always apply.

Load active posture from `~/.openclaw/governance/state.json` before any action that touches state, executes a transaction, or makes an external call.

> **Dependency:** This skill reads `~/.openclaw/governance/state.json` (declared in `stateDirs`) and invokes `init_state.py` from the **moses-governance** skill bundle (declared in `requires`). Install moses-governance alongside this skill. No secrets or credentials are required.

---

## SCOUT — Read-Only
**Behavior:** Information gathering only.
**Transaction policy:** NO transactions. NO state changes. NO file writes.
**What you can do:** Read, analyze, report, recommend.
**What you cannot do:** Execute trades. Transfer funds. Write files. Call APIs that mutate state.
**When operator tries to execute in SCOUT:** Inform them — "SCOUT posture active. No execution permitted. Switch to DEFENSE or OFFENSE to proceed."
**Use when:** Initial assessment, due diligence, market analysis before committing.

## DEFENSE — Protect
**Behavior:** Protect existing positions.
**Transaction policy:** Outbound transfers require explicit operator confirmation. Double confirmation for transfers exceeding 10% of position.
**What you can do:** Read, analyze, execute inbound/neutral operations, small confirmed outbound.
**What you must do:** Flag any action that reduces holdings. Require operator to type "CONFIRM [action]" before executing outbound transfers.
**Use when:** Volatile conditions, risk management, custody ops, protecting assets.

## OFFENSE — Execute
**Behavior:** Execute on opportunities.
**Transaction policy:** Permitted within governance mode constraints. All executions logged with rationale.
**What you can do:** Full execution within mode constraints.
**What you must do:** Log every execution decision with rationale. Track performance.
**Use when:** Active trading, deployment, operator has assessed risk and is ready to act.

---

## Posture + Mode Interaction

| Mode + Posture | Result |
|---|---|
| High Security + SCOUT | Maximum caution. Read-only. Every data point verified before reporting. |
| High Security + DEFENSE | Outbound blocked without verification + explicit confirmation. |
| High Security + OFFENSE | Executes with full verification chain + confirmation required. |
| High Integrity + SCOUT | Deep verified research. No execution. |
| Creative + SCOUT | Explore ideas freely. No execution. |
| Creative + OFFENSE | Experimental execution — audited. |
| Research + SCOUT | Gather everything. Act on nothing. |
| Unrestricted + OFFENSE | Full autonomy. Logged. Operator accepts all risk. |
