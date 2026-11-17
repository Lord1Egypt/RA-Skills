<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# AI-FLO — Agent Shortcut Rules Block

**Purpose:** Copy this block into your workspace's `.kiro/steering/workspace-rules.md` to enable the FIA__ shortcut.

---

## Block (Copy Between Markers)

```markdown
<!-- BEGIN AI-FLO AGENT SHORTCUTS -->

### AI-FLO Agents

| Shortcut | Agent | Purpose |
|----------|-------|---------|
| `FIA__` | Flow Integrity Agent | On-demand validation of routing state, table integrity, conflict resolution, and topology consistency |

**Rule:** When the user types `FIA__` (uppercase, with double underscore) anywhere in a prompt, immediately invoke the Flow Integrity Agent (`.kiro/agents/flow-integrity-agent.md`) and execute its full 17-check integrity pass. No further clarification needed — treat `FIA__` as a direct command to run the agent.

<!-- END AI-FLO AGENT SHORTCUTS -->
```

---

## Installation Notes

1. This block is additive — paste it into your existing workspace rules without removing other agent shortcuts
2. The agent file (`flow-integrity-agent.md`) must exist at `.kiro/agents/flow-integrity-agent.md`
3. The shortcut follows the same pattern as IQA__, ADA__, WIA__, UXC__ (family convention)

---

*Part of AI-FLO v1.0.0*
