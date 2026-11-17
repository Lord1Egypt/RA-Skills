<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
---
generatedBy: AI-PILC
generatedVersion: "{version}"
source: ai-pilc-rules/core-workflow.md
generatedOn: "{ISO-date}"
ownership: generated
purpose: Appended to destination workspace's .governance/AGENT-GUIDE.md
---

<!-- BEGIN AI-PILC AGENT GUIDE SECTION -->

## AI-PILC — Initiation Quality Agent (`IQA__`)

### What It Does

Validates that your Project Initiation Package (PIP) meets professional PMO quality standards before it leaves the initiation phase. Think of it as a final quality gate — the governance equivalent of a code review, but for project documentation.

### When to Call

| Trigger | Process Milestone | Why Now |
|---------|-------------------|---------|
| `IQA__` | After PIP completion (Stage 16) | Full package validation before handoff |
| `IQA__` | After PLANNING phase (Stage 14) | Mid-workflow checkpoint for complex projects |
| `IQA__` | Before Steering Committee review | Ensures presentation-grade quality |
| `IQA__` | Before AI-ADLC handoff | Confirms architecture can safely consume the PIP |

**How to call:** Type `IQA__` anywhere in your chat prompt. The agent activates immediately.

### What It Checks

| Category | Checks | What "Pass" Means |
|----------|--------|-------------------|
| **Completeness** | All mandatory deliverables present; conditional artifacts present when applicable; no unresolved TBDs; state file complete | Every expected artifact exists and is filled |
| **Gate Compliance** | Every stage completion logged as user-approved decision; skips documented with rationale; depth level matches deliverable richness | The workflow was followed as designed |
| **Stakeholder Coverage** | ≥3 stakeholders registered; Power/Interest classified; RACI roles map to registered people | Governance accountability is clear |
| **Register Integrity** | Decision Log populated (≥2 entries); sequential numbering correct; cross-register references resolve; spine marker present (chain mode) | Audit trail is complete and consistent |
| **Cross-References** | Inter-artifact references resolve; Project ID consistent across all documents | No broken links between deliverables |

### What Breaks If You Skip

| Impact | Description | Detection |
|--------|-------------|-----------|
| 🟠 Incomplete handoff | AI-ADLC builds architecture on partial requirements | When ADLC asks questions already answered in missing PIP docs |
| 🟡 Broken audit trail | Decisions made but not logged → no rationale for future teams | Next compliance audit flags missing entries |
| 🟡 Stakeholder gaps | Key people not engaged → scope changes, rework later | Mid-project when they surface concerns |
| 🟢 Cross-ref breaks | Documents reference non-existent artifacts → confusing package | When someone tries to follow the trail |

### Recovery

**If you forgot to call `IQA__` and the PIP is already in use:**

1. Run `IQA__` now — it checks the current state of all artifacts
2. For missing deliverables: author retroactively, log as post-initiation addition
3. For register gaps: review `pilc-state.md` history, backfill entries
4. For stakeholder gaps: add to register, schedule catch-up engagement
5. If AI-ADLC already started: communicate any PIP updates that may affect architecture

**Self-healing?** ⚠️ Partial — the agent checks current state, but it cannot reconstruct decisions or approvals that were never recorded.

### Relationship to Other Agents

| Agent | Relationship |
|-------|-------------|
| `session-discipline-agent` (AI-GCE) | SDC checks **process methodology**; IQA checks **artifact quality** — complementary |
| `compliance-audit-agent` (AI-GCE) | Full audit covers everything including PIP quality — IQA is the focused, faster check |
| `architecture-decision-agent` (AI-ADLC) | ADA validates what ADLC produces; IQA validates what ADLC **consumes** |

### Output

- **Pass:** One-line summary confirming PIP is ready + check counts
- **Violations:** Per-check report with ID, status, finding, and remediation suggestion
- **Log:** Entry in `.governance/compliance-log/events/` (if governance infra exists)

<!-- END AI-PILC AGENT GUIDE SECTION -->
