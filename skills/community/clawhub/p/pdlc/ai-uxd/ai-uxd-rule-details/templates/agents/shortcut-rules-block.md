<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# AI-UXD — Shortcut Rules Block

> This content is appended to the target workspace's `.kiro/steering/workspace-rules.md`
> between package-specific markers. AI-UXD's installation step inserts this block.

---

## Template Content (Insert Between Markers)

```markdown
<!-- BEGIN AI-UXD AGENT SHORTCUTS -->

### AI-UXD Governance Agent

| Trigger | Agent | Purpose |
|---------|-------|---------|
| `UXC__` | UX Consistency Agent | Validates UXP internal consistency, traceability, token alignment, accessibility spec match, and handoff consumability |

**Usage:** Type `UXC__` in any prompt to invoke the UX Consistency Agent. It runs autonomously and produces a consistency report.

**When to use:**
- After revising any UXP artifact
- Before downstream handoffs (AI-POLC, AI-DWG, AI-GCE)
- After incorporating AI-DLC v1 feedback
- Monthly governance check

<!-- END AI-UXD AGENT SHORTCUTS -->
```

---

## Installation Logic

When AI-UXD completes package assembly (Stage 16), the installation step:

1. **Installs agent:** Copy `ux-consistency-agent.md` → `.kiro/agents/ux-consistency-agent.md`
2. **Registers shortcut:** Append the above block into `.kiro/steering/workspace-rules.md` (between `<!-- BEGIN AI-UXD -->` / `<!-- END AI-UXD -->` markers — create if absent, append if markers don't exist)
3. **Updates AGENT_REGISTRY.md:** Create `.governance/AGENT_REGISTRY.md` if absent; append AI-UXD entries using `UXD-AG-{NN}` IDs
4. **Updates AGENT-GUIDE.md:** Create `.governance/AGENT-GUIDE.md` if absent; append AI-UXD section (when to call, consequences, recovery)

---

## Agent ID Convention

| Package | ID Prefix | Example |
|---------|-----------|---------|
| AI-UXD | `UXD-AG-` | `UXD-AG-01` |

Each package numbers its own agents independently (`{PKG}-AG-{NN}`). No global range allocation needed — the prefix prevents collisions regardless of installation order.
