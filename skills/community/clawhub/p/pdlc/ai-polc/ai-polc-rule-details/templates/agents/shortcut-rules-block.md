<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# AI-POLC — Shortcut Rules Block

> This content is appended to the target workspace's `.kiro/steering/workspace-rules.md`
> between package-specific markers. AI-POLC's installation step inserts this block.

---

## Template Content (Insert Between Markers)

```markdown
<!-- BEGIN AI-POLC AGENT SHORTCUTS -->

### AI-POLC Governance Agent

| Trigger | Agent | Purpose |
|---------|-------|---------|
| `BLH__` | Backlog Health Agent | Validates backlog structure/vision integrity, prioritization coherence (rationale-backed), DoR/DoD quality bar, traceability/lineage, and downstream handoff readiness |

**Usage:** Type `BLH__` in any prompt to invoke the Backlog Health Agent. It runs autonomously and produces a backlog-health report.

**When to use:**
- After PBP assembly, before status = `ready` (handoff to AI-DWG)
- Before each sprint/increment refinement
- After reprioritization or DoR/DoD changes
- Per-release backlog-health check

<!-- END AI-POLC AGENT SHORTCUTS -->
```

---

## Installation Logic

When AI-POLC completes PBP assembly (Stage 13) — or at any point during execution — the installation step:

1. **Installs agent:** Copy `backlog-health-agent.md` → `.kiro/agents/backlog-health-agent.md` (populate `{version}` + `{ISO-date}`)
2. **Registers shortcut:** Append the above block into `.kiro/steering/workspace-rules.md` (between `<!-- BEGIN AI-POLC AGENT SHORTCUTS -->` / `<!-- END AI-POLC AGENT SHORTCUTS -->` markers — replace if present, append if absent)
3. **Updates AGENT_REGISTRY.md:** Create `.governance/AGENT_REGISTRY.md` if absent; append the AI-POLC entry using `POLC-AG-{NN}` IDs
   - Entry: `| POLC-AG-01 | backlog-health-agent | Process | BLH__ | 1 | AI-POLC | Active | {date} |`
4. **Updates AGENT-GUIDE.md:** Create `.governance/AGENT-GUIDE.md` if absent; append the AI-POLC section from `agent-guide.md` (between `<!-- BEGIN AI-POLC AGENT GUIDE SECTION -->` markers)

---

## Agent ID Convention

| Package | ID Prefix | Example |
|---------|-----------|---------|
| AI-POLC | `POLC-AG-` | `POLC-AG-01` |

Each package numbers its own agents independently (`{PKG}-AG-{NN}`). No global range allocation needed — the prefix prevents collisions regardless of installation order.
