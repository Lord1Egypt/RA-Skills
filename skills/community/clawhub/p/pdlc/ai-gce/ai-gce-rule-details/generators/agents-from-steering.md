<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
---
generatedBy: AI-GCE
generatedVersion: 1.0.0
source: ai-gce-rules/core-generator.md
generatedOn: 2026-06-11
ownership: generated
---

# Agent Derivation Logic — Process & Audit Agents from Steering

**Purpose:** Derive and generate process/audit agents from workspace steering files. This is the agent-generation counterpart to `hooks-from-steering.md`. While hooks handle automatic, real-time enforcement, agents handle milestone-based governance that requires human-triggered invocation.

**Design Principle:** "Can the user trigger this themselves with a keyword instead of it firing automatically?" If yes → agent, not hook. Process governance checks are milestone-based — only the user knows when a sprint boundary, a review, or a release is happening.

---

## Agent Generation Strategy

### When This Generator Runs

- **Mode 1 (Full Generation):** Generate all agents per tier activation
- **Mode 2 (Re-Derivation):** Update affected agents when steering changes
- **Mode 3 (Brownfield):** Generate with brownfield-aware adaptations
- **Mode 4 (Tier Activation):** Unlock tier-gated agents

### What This Generator Reads

| Steering File | Agent(s) Derived | Trigger | Content Extracted |
|---------------|-----------------|---------|-------------------|
| `session-governance.md` | `session-discipline-agent` | `SDC__` | Session methodology rules, correction escalation, context protocol |
| `project-governance.md` | `sprint-governance-agent`, `change-management-agent` | `SGV__`, `CMG__` | Sprint cadence, gate criteria, release governance |
| `git-workflow.md` + `role-isolation.md` | `code-review-agent` | `CRV__` | Review requirements, trust spectrum, role separation |
| `TEAM_AGREEMENTS.md` | `code-review-agent`, `sprint-governance-agent` | `CRV__`, `SGV__` | Team-specific agreements on review, sprint ceremonies |
| Self-derived (all `rules/`) | `steering-quality-agent` | `SQC__` | Meta-governance (checks the steering files themselves) |
| `DEFINITION_OF_DONE.md` | `dod-gate-agent` | `DOD__` | DoD checklist items, acceptance criteria patterns |
| `testing-strategy.md` | `dod-gate-agent` | Test evidence requirements |

---

## For EACH Agent to Generate

### Step 1: Determine Applicability

```
IF session-governance.md EXISTS
   → Generate session-discipline-agent (Tier 1)
ELSE
   → Generate session-discipline-agent with BUILT-IN BASELINE only (Tier 1)
   (Session discipline is universal — never skip it even without steering)

IF project-governance.md EXISTS AND mentions "sprint" or "iteration"
   → Generate sprint-governance-agent (Tier 2)
ELSE
   → Skip sprint-governance-agent (no sprint cadence detected)

IF git-workflow.md EXISTS OR role-isolation.md EXISTS
   → Generate code-review-agent (Tier 2)
ELSE
   → Generate code-review-agent with BASELINE only (Tier 2)
   (Review governance is universal for teams ≥ 2)

FOR steering-quality-agent:
   → ALWAYS generate (Tier 2) — it checks the steering files themselves

IF project-governance.md EXISTS AND mentions "release" or "deployment" or "go-live"
   → Generate change-management-agent (Tier 3)
ELSE
   → Skip change-management-agent (no release governance detected)

IF DEFINITION_OF_DONE.md EXISTS
   → Generate dod-gate-agent with project-specific criteria (Tier 2)
ELSE
   → Generate dod-gate-agent with BASELINE DoD only (Tier 2)
```

### Step 2: Load Template

For each applicable agent, load the template from:
```
templates/agents/{agent-name}.md
```

### Step 3: Populate Template

Replace `{placeholder}` values with project-specific content:

| Placeholder | Source |
|-------------|--------|
| `{version}` | AI-GCE version from core-generator |
| `{ISO-date}` | Current date |
| `{project_name}` | From `PROJECT_INSTRUCTIONS.md` or workspace root folder name |

**For steering-enriched content:**
- Extract SPECIFIC rules, criteria, and thresholds from the steering file
- Replace generic check descriptions with project-specific ones
- Add project-specific DoD items, review requirements, sprint expectations

### Step 4: Install Agents

```
Install to:.governance/agents/{agent-name}.md
```

Rules:
- Overwrite existing generated agents (check `ownership: generated` in front-matter)
- NEVER overwrite agents with `ownership: hybrid` or `ownership: user`
- If agent already exists with custom content: MERGE (preserve `<!-- custom -->` sections)

### Step 5: Generate AGENT-GUIDE.md

Load template from: `templates/agents/agent-guide.md`

Populate with:
- Only the agents that were actually generated (skip rows for skipped agents)
- Project-specific examples in "When to Call"
- Correct tier assignments
- Actual rule IDs from generated rules

```
Install to:.governance/AGENT-GUIDE.md
```

### Step 6: Generate AGENT_REGISTRY.md

Load template from: `templates/agents/agent-registry.md`

Populate with:
- All generated agents with their details
- Correct tier assignments
- Current date for "Last Updated"
- Preserve `<!-- custom -->` section from existing registry (if re-deriving)

```
Install to:.governance/AGENT_REGISTRY.md
```

### Step 7: Register Shortcuts in Workspace Rules

For each generated agent that has a `trigger` field:
- Check if `rules/workspace-rules.md` exists
- If YES: append the shortcut rules block from the template (preserve existing content)
- If NO: create a minimal workspace-rules with the shortcut block

**Template:** Load `templates/agents/shortcut-rules-block.md` and append its content
(between the `<!-- BEGIN AI-GCE AGENT SHORTCUTS -->` and `<!-- END AI-GCE AGENT SHORTCUTS -->` markers)
to the destination workspace's `rules/workspace-rules.md`.

**Re-derivation behavior:** If the markers already exist in workspace-rules, REPLACE the content
between them (overwrite with updated shortcut block). Content outside the markers is preserved.

**Tier filtering:** Include ALL shortcuts in the block regardless of current tier.
The agent itself handles tier-gating (responds with "activates at Tier N" if invoked early).
This avoids needing to re-edit workspace-rules on every tier upgrade.

---

## Re-Derivation Behavior (Mode 2)

When steering files change and AI-GCE re-derives:

1. **Read existing agents** — check front-matter for `ownership`
2. **If `ownership: generated`** — safe to overwrite with updated derivation
3. **If `ownership: hybrid`** — preserve `<!-- custom -->` sections, update generated sections
4. **If agent no longer applicable** (e.g., sprint governance steering removed) — mark as `Inactive` in registry, do NOT delete file
5. **Update AGENT-GUIDE.md** — regenerate from current agent set
6. **Update AGENT_REGISTRY.md** — update status/dates, preserve custom rows

---

## Brownfield Adaptations (Mode 3)

When generating agents for brownfield workspaces:

- `session-discipline-agent`: Add check for "existing code without specs → flag as acknowledged debt, don't fail"
- `sprint-governance-agent`: No brownfield adaptation needed (sprint process is forward-looking)
- `code-review-agent`: Add check for "legacy code review standard may differ from new standard"
- `steering-quality-agent`: Add check for "brownfield-patterns.md freshness"
- `change-management-agent`: Add check for "incremental adoption plan compliance"
- `dod-gate-agent`: Add check for "brownfield debt acknowledged vs. new code DoD"

---

## Validation Checklist

After generating all agents, verify:

- [ ] Each agent follows the anatomy defined in `AGENT_GOVERNANCE_CONTRACT.md` §4
- [ ] Front-matter is complete (all required fields present)
- [ ] Tier assignments are correct (1 for Day 0, 2 for Sprint 2+, 3 for Pre-Release)
- [ ] AGENT-GUIDE.md includes all generated agents (and only those)
- [ ] AGENT_REGISTRY.md lists all agents with correct metadata
- [ ] Shortcuts are registered in workspace-rules
- [ ] No overlap with hook coverage (agents don't duplicate what hooks already check automatically)
- [ ] Project-specific content replaces generic placeholders
- [ ] `<!-- custom -->` markers present in guide and registry for team additions

---

*This generator is the agent equivalent of `hooks-from-steering.md`. It runs during Steps 5c/5d of the Full Generation flow (Mode 1) and during re-derivation (Mode 2).*
