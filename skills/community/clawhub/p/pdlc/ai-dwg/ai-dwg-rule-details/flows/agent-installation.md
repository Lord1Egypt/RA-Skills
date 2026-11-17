<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Post-Generation: Agent Installation

## Purpose

The orchestration logic for installing the AI-DWG governance agent into the destination workspace after any generation or reconciliation completes (Mode 1, 2, or 3). This step is **automatic** — no user interaction required. The core (`core-generator.md`) carries the pointer + the `WIA__` trigger name; this file carries the install steps. Templates live in `templates/agents/` (`workspace-integrity-agent.md`, `shortcut-rules-block.md`, `agent-guide.md`).

---

## What Gets Installed

| Artifact | Destination | Action |
|----------|-------------|--------|
| `workspace-integrity-agent.md` | `.kiro/agents/` | Copy from `templates/agents/` |
| Shortcut rules block | `rules/workspace-rules.md` | Append `<!-- BEGIN AI-DWG AGENT SHORTCUTS -->` block (or replace if exists) |
| Agent registry entries | `.governance/AGENT_REGISTRY.md` | Create file if absent; append AI-DWG entries if exists |
| Agent guide section | `.governance/AGENT-GUIDE.md` | Create file if absent; append AI-DWG section if exists |

## Installation Logic

1. **Agent file:** Copy `templates/agents/workspace-integrity-agent.md` to `.kiro/agents/workspace-integrity-agent.md`. Populate `{version}` with current AI-DWG version and `{ISO-date}` with today's date.

2. **Shortcut block:** Check `rules/workspace-rules.md` for `<!-- BEGIN AI-DWG AGENT SHORTCUTS -->` marker:
   - If found → replace the block (between BEGIN and END markers)
   - If not found → append the block from `templates/agents/shortcut-rules-block.md`

3. **Agent registry:** Check for `.governance/AGENT_REGISTRY.md`:
   - If absent → create with header + AI-DWG entry (DWG-AG-01)
   - If exists → append AI-DWG entry using next available `DWG-AG-{NN}` ID
   - Entry: `| DWG-AG-01 | workspace-integrity-agent | Audit | WIA__ | 1 | AI-DWG | Active | {date} |`

4. **Agent guide:** Check for `.governance/AGENT-GUIDE.md`:
   - If absent → create with header + AI-DWG section from `templates/agents/agent-guide.md`
   - If exists → append AI-DWG section (between `<!-- BEGIN AI-DWG AGENT GUIDE SECTION -->` markers)

## Self-Sufficiency Rule (AGENT_GOVERNANCE_CONTRACT §5)

AI-DWG installs its own agent independently. No dependency on AI-GCE or any other package being present. If other packages run later, they will detect and preserve the AI-DWG entries via marker-based ownership.

## Post-Install Confirmation

```
🤖 AI-DWG Governance Agent Installed
   • Agent: workspace-integrity-agent (DWG-AG-01)
   • Shortcut: WIA__ (active immediately)
   • Call WIA__ after generation/reconciliation to validate workspace integrity.
```

---

*Post-generation step — loaded + executed by `core-generator.md` after Mode 1/2/3 completes.*
