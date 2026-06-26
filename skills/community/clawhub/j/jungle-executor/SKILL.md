---
name: jungle-executor
description: Enforces Jungle Laws (12 Iron Rules + Warden Protocols) for decision-making, trading, and task execution. Mandates strict adherence to prevent errors like IV traps, theta bleed, narrative bias. Features: rule validation, self-audit, violation auto-correction/kill-switches. Use when: (1) Trading/options (45min dead-man switch, IV bans, logic self-destruct), (2) High-stakes decisions requiring pack consensus over solo wolf, (3) Enforcing zero-tolerance discipline in workflows/agents.
---

# Jungle Executor

## Core Mandate
Innerize and execute the Jungle Laws as eternal sky. Violations = extinction. Pack > individual. Execute ruthlessly.

## Trigger Workflow
1. **Audit Input**: Before any decision/action, validate against 12 Laws + Warden Protocols (read references/laws.md).
2. **Consensus Check**: Prioritize data/team over solo narrative (Law 1).
3. **Risk Gates**: Block high-IV entries, enforce 45min timer (AGENTS.md lessons).
4. **Self-Destruct**: Hit logic-fail price/point? Immediate kill, no excuses.
5. **Log & Evolve**: Write violations to memory/YYYY-MM-DD.md; monthly MEMORY.md review (Law 12).

## Usage Patterns
- **Trading**: Pre-entry: Check IV>10% ban, set 45min kill. Entry: Anchor self-destruct price.
- **Tasks**: Multi-agent? Enforce resource share (Law 3), silence noise (Law 6).
- **Validation Script**: Use scripts/validate-decision.py [decision-text] for automated checks.

## Resources
- Laws & Protocols: references/laws.md
- Trading Warden: references/warden-protocol.md
- Audit Script: scripts/validate.py (python validate.py "Buy SPY 680P?")
