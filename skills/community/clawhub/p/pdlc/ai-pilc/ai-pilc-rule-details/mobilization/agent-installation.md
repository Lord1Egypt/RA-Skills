<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Post-Workflow: Agent Installation

## Execution: ALWAYS (automatic — no user interaction required)

After the PIP workflow completes (or at any point during AI-PILC execution), install the AI-PILC governance agent into the destination workspace.

---

## What Gets Installed

| Artifact | Destination | Action |
|----------|-------------|--------|
| `initiation-quality-agent.md` | `.kiro/agents/` | Copy from `templates/agents/` |
| Shortcut rules block | `.kiro/steering/workspace-rules.md` | Append `<!-- BEGIN AI-PILC AGENT SHORTCUTS -->` block (or replace if exists) |
| Agent registry entries | `.governance/AGENT_REGISTRY.md` | Create file if absent; append AI-PILC entries if exists |
| Agent guide section | `.governance/AGENT-GUIDE.md` | Create file if absent; append AI-PILC section if exists |

---

## Installation Logic

1. **Agent file:** Copy `templates/agents/initiation-quality-agent.md` to `.kiro/agents/initiation-quality-agent.md`. Populate `{version}` with current AI-PILC version and `{ISO-date}` with today's date.

2. **Shortcut block:** Check `.kiro/steering/workspace-rules.md` for `<!-- BEGIN AI-PILC AGENT SHORTCUTS -->` marker:
   - If found → replace the block (between BEGIN and END markers)
   - If not found → append the block from `templates/agents/shortcut-rules-block.md`

3. **Agent registry:** Check for `.governance/AGENT_REGISTRY.md`:
   - If absent → create with header + AI-PILC entry (PILC-AG-01)
   - If exists → append AI-PILC entry using next available `PILC-AG-{NN}` ID
   - Entry: `| PILC-AG-01 | initiation-quality-agent | Process | IQA__ | 1 | AI-PILC | Active | {date} |`

4. **Agent guide:** Check for `.governance/AGENT-GUIDE.md`:
   - If absent → create with header + AI-PILC section from `templates/agents/agent-guide.md`
   - If exists → append AI-PILC section (between `<!-- BEGIN AI-PILC AGENT GUIDE SECTION -->` markers)

---

## Self-Sufficiency Rule (AGENT_GOVERNANCE_CONTRACT §5)

AI-PILC installs its own agent independently. No dependency on AI-GCE being present. If AI-GCE runs later, it will detect and preserve the AI-PILC entries via marker-based ownership.

---

## Post-Install Confirmation

```
🤖 AI-PILC Governance Agent Installed
   • Agent: initiation-quality-agent (PILC-AG-01)
   • Shortcut: IQA__ (active immediately)
   • Call IQA__ after PIP completion to validate package quality.
```
