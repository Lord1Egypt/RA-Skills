---
name: moses-modes
description: "MO§ES™ Governance Modes — Injects behavioral constraints from the active mode into all agent prompts. 8 modes: high-security, high-integrity, creative, research, self-growth, problem-solving, idk, unrestricted. Part of the moses-governance bundle. Patent pending Serial No. 63/877,177."
metadata:
  openclaw:
    emoji: 🎛️
    tags: [governance, modes, constraints, behavioral]
    version: 0.1.2
    stateDirs:
      - ~/.openclaw/governance
    requires:
      - moses-governance
example: |
  # Set mode via operator command: /govern high-security
  # Or directly: python3 ~/.openclaw/workspace/skills/moses-governance/scripts/init_state.py set --mode high-security
---

# MO§ES™ Governance Modes

Load active mode from `~/.openclaw/governance/state.json` before every action.
Apply the constraints below as governance guardrails. These constraints block prohibited action categories (e.g. speculative responses in High Security, unverified transactions in High Integrity) — they do not override core task instructions or general operator requests outside the prohibited categories.

> **Dependency:** Reads `~/.openclaw/governance/state.json` (declared in `stateDirs`). The `/govern` command calls `init_state.py` from the **moses-governance** skill bundle (declared in `requires`). No secrets or credentials required.
