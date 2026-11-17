<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
---
generatedBy: AI-ILC
generatedVersion: "{version}"
source: ai-ilc-rules/core-workflow.md
generatedOn: "{ISO-date}"
ownership: generated
purpose: Appended to destination workspace's .governance/AGENT-GUIDE.md
---

<!-- BEGIN AI-ILC AGENT GUIDE SECTION -->

## AI-ILC — Idea Quality Agent (`IQC__`)

### What It Does

Validates that the output from AI-ILC (Approved Idea Brief, Feature Brief, or Change Request Brief) meets professional innovation-governance standards before it proceeds to the next lifecycle stage. Think of it as the quality gate for idea-stage decisions — ensuring nothing enters the project pipeline without proper evaluation and documentation.

### When to Call

| Trigger | Process Milestone | Why Now |
|---------|-------------------|---------|
| `IQC__` | After idea evaluation complete (Stage 6) | Full brief validation before handoff |
| `IQC__` | After Evaluate stage (Stage 3) | Mid-workflow — ensures scoring is solid before scoping |
| `IQC__` | Before AI-PILC handoff | Confirms Approved Idea Brief is ready for project initiation |
| `IQC__` | Before AI-POLC handoff | Confirms Feature Brief is ready for backlog management |

**How to call:** Type `IQC__` anywhere in your chat prompt. The agent activates immediately.

### What It Checks

| Category | Checks | What "Pass" Means |
|----------|--------|-------------------|
| **Completeness** | Output brief exists for the declared route; all mandatory sections populated; state file complete; no unresolved placeholders | Every expected artifact exists and is filled |
| **Evaluation Integrity** | All scoring dimensions completed; each score has rationale; go/no-go decision formally recorded | Decision is defensible and auditable |
| **Routing Quality** | Route field present in state; route rationale documented; handoff context sufficient for receiving package | Downstream package can start without confusion |
| **Governance Records** | Decision log populated; sequential numbering correct; spine-aware prefixing (if chain mode) | Audit trail is intact from the very first lifecycle moment |

### What Breaks If You Skip

| Impact | Description | Detection |
|--------|-------------|-----------|
| 🟠 Weak foundations | AI-PILC builds a project on an idea brief that was never validated | When PILC asks questions already answered (or not answered) in the brief |
| 🟡 Indefensible decision | Idea approved but no one can explain why (vs. rejected alternatives) | When portfolio review questions prioritization |
| 🟡 Route confusion | Feature sent to AI-PILC (should be AI-POLC) or vice versa | When receiving package determines the scope doesn't match its purpose |
| 🟢 Audit gap | No governance record of the idea-stage approval | When compliance audit runs and finds no trail before project initiation |

### Recovery

**If you forgot to call `IQC__` and the idea is already downstream:**

1. Run `IQC__` now — it checks the current state of all ILC artifacts
2. For missing brief sections: backfill from `ilc-state.md` and original input
3. For scoring gaps: re-evaluate using the criteria, record scores retroactively
4. For routing rationale: document why this route was chosen, mark as "retrospective"
5. If AI-PILC already started: communicate any clarifications that affect initiation scope

**Self-healing?** ⚠️ Partial — the agent validates current state but cannot reconstruct scoring rationale that was never recorded.

### Relationship to Other Agents

| Agent | Relationship |
|-------|-------------|
| `initiation-quality-agent` (AI-PILC) | IQC validates what feeds INTO PILC; IQA validates what PILC PRODUCES — sequential |
| `compliance-audit-agent` (AI-GCE) | Full audit covers everything; IQC is the focused, faster check for idea-stage specifically |
| `portfolio-governance-agent` (AI-PPM) | PPM governs the set of projects; IQC ensures each idea is quality-checked before entering that set |

### Output

- **Pass:** One-line summary confirming brief is ready + check counts
- **Violations:** Per-check report with ID, status, finding, and remediation suggestion
- **Log:** Entry in `.governance/compliance-log/events/` (if governance infra exists)

<!-- END AI-ILC AGENT GUIDE SECTION -->
