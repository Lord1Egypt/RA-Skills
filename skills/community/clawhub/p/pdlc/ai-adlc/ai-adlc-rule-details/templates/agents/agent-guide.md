<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
---
generatedBy: AI-ADLC
generatedVersion: "{version}"
source: ai-adlc-rules/core-workflow.md
generatedOn: "{ISO-date}"
ownership: generated
purpose: Appended to destination workspace's .governance/AGENT-GUIDE.md
---

<!-- BEGIN AI-ADLC AGENT GUIDE SECTION -->

## AI-ADLC — Architecture Decision Agent (`ADA__`)

### What It Does

Validates that your Architecture Package (AP) meets professional architecture quality standards before it leaves the design phase. Think of it as the architecture equivalent of a code review — a systematic quality gate ensuring your design decisions are complete, traceable, consistent, and ready for downstream consumption.

### When to Call

| Trigger | Process Milestone | Why Now |
|---------|-------------------|---------|
| `ADA__` | After AP completion (Stage 13) | Full package validation before handoff |
| `ADA__` | After DECISIONS phase (Stage 8) | Mid-workflow checkpoint for complex systems |
| `ADA__` | Before development team onboarding | Ensures architecture is presentation-grade |
| `ADA__` | Before AI-DWG handoff | Confirms `adlc-state.md` and artifacts are AI-DWG-ready |

**How to call:** Type `ADA__` anywhere in your chat prompt. The agent activates immediately.

### What It Checks

| Category | Checks | What "Pass" Means |
|----------|--------|-------------------|
| **ADR Quality** | Major decisions have ADRs; format compliant; sequential numbering; status consistent; cross-references link | Every significant technology/pattern choice is documented with rationale |
| **C4 Level Consistency** | System Context complete; Container integrity; Component-to-Container alignment; progressive detail validated | The C4 model is internally consistent from L1 through L3 |
| **Decision Traceability** | Requirements → decisions linked; decisions → artifacts linked; constraints propagated | You can trace any architecture choice back to a requirement and forward to its implementation |
| **Cross-Reference Integrity** | Inter-document references resolve; technology consistency; security coverage; integration completeness | No broken links, no orphaned references, no forgotten systems |
| **Extension Compliance** | Activated extensions enforced; extensions coherent with base architecture | Opted-in patterns (DDD, Microservices, etc.) are actually reflected in the design |
| **State File & Downstream Readiness** | State file complete; AI-DWG signal fields populated; management registers present | AI-DWG can consume the AP without guessing missing context |

### What Breaks If You Skip

| Impact | Description | Detection |
|--------|-------------|-----------|
| 🔴 Incomplete handoff | AI-DWG generates workspace from inconsistent architecture | When steering files contradict each other or reference non-existent modules |
| 🟠 Lost rationale | Technology decisions made but not recorded in ADRs | When someone asks "why did we choose X?" and there's no answer |
| 🟠 C4 drift | Components reference containers that were renamed or removed | When developers can't find the module their component belongs to |
| 🟡 Extension mismatch | DDD extension activated but no bounded contexts defined | When implementation diverges from declared architectural style |
| 🟡 Broken state file | AI-DWG reads incomplete `adlc-state.md` → partial steering | When workspace is missing technology-specific rules or extension steering |

### Recovery

**If you forgot to call `ADA__` and the AP is already in use:**

1. Run `ADA__` now — it checks the current state of all AP artifacts
2. For missing ADRs: reconstruct from Architecture Workbook entries or conversation history
3. For C4 misalignment: update the affected level document to reconcile references
4. For state file gaps: update `adlc-state.md` with missing extension/container/constraint fields
5. If AI-DWG already generated: communicate corrections that affect steering; consider targeted reconciliation

**Self-healing?** ⚠️ Partial — the agent checks current state and identifies gaps, but it cannot reconstruct decision rationale that was never captured.

### Relationship to Other Agents

| Agent | Relationship |
|-------|-------------|
| `initiation-quality-agent` (AI-PILC) | IQA validates what AI-ADLC **consumes**; ADA validates what AI-ADLC **produces** |
| `workspace-integrity-agent` (AI-DWG) | WIA validates workspace structure **generated from** the AP; ADA validates the AP itself |
| `session-discipline-agent` (AI-GCE) | SDC checks **process methodology**; ADA checks **architecture artifact quality** — complementary |
| `compliance-audit-agent` (AI-GCE) | Full audit covers everything including architecture quality — ADA is the focused, faster check |

### Output

- **Pass:** One-line summary confirming AP is ready + check counts
- **Violations:** Per-check report with ID, status, finding, and remediation suggestion
- **Log:** Entry in `.governance/compliance-log/events/` (if governance infra exists)

<!-- END AI-ADLC AGENT GUIDE SECTION -->
