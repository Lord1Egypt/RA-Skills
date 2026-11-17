# Anatomy of a State File

**Purpose:** Field-by-field breakdown of AI-* Family state files — what each field means, when it's set, who reads it, and how to reconstruct one if lost.

**Derived from:** Pattern: Marker File Detection + Pattern: Gate Before Transition

---

## What a State File Is

A state file is a persistent markdown document that serves TWO roles simultaneously:
1. **Session continuity** — tells any AI session where to resume
2. **Chain marker** — tells successor packages that this output exists and what it contains

Every lifecycle package produces one. Its filename is non-negotiable.

---

## Universal Fields (All State Files)

```markdown
# {Package} State

## Project Identity
- Project ID: PRJ-ACME-2026-001
- Project Name: Acme Platform Modernization

## Progress
- Current Phase: PLANNING
- Current Stage: 8 (Resource Planning)
- Status: In Progress
- Workflow Depth: Standard
- Output Structure: numbered

## Completed Stages
| Stage | Name | Completed | Gate Approved By |
|:-----:|------|-----------|-----------------|
| 1 | Workspace Detection | 2026-06-10 09:15 | auto |
| 2 | Source Ingestion | 2026-06-10 09:45 | User |
| 3 | Requirement Structuring | 2026-06-10 10:30 | User |
| ... | ... | ... | ... |

## Session History
- Last Session: 2026-06-11 14:00
- Total Sessions: 3
- Session Platform: Kiro
```

---

## Field-by-Field Reference

### Project Identity

| Field | Set When | Changed When | Read By |
|-------|----------|-------------|---------|
| `Project ID` | Stage 1 (minted) | Never (immutable) | All successor packages (correlation key) |
| `Project Name` | Stage 1 | Rarely (rename only) | Successor packages (display/context) |

**Project ID format:** `PRJ-{ABBREVIATION}-{YEAR}-{SEQUENCE}`
- Minted by AI-PILC (or AI-ILC if it runs first)
- Carried forward through the entire chain
- Used by AI-PPM for portfolio roll-up

### Progress

| Field | Set When | Changed When | Purpose |
|-------|----------|-------------|---------|
| `Current Phase` | Stage 1 | Every phase boundary | Resume: which phase are we in? |
| `Current Stage` | Stage 1 | Every stage completion (gate pass) | Resume: which stage is next? |
| `Status` | Creation | Workflow milestones | `In Progress` / `Complete` / `Paused` / `Abandoned` |
| `Workflow Depth` | Stage 2 (ingestion) | Rarely (depth override) | Controls stage behavior for all remaining stages |
| `Output Structure` | Stage 1 | Never (once set) | `numbered` / `flat` — tells successors the internal deliverable sub-structure pattern |

### Completed Stages

| Field | Purpose |
|-------|---------|
| Stage number | Which stage completed |
| Name | Human-readable stage name |
| Completed timestamp | When gate was passed (ISO date or datetime) |
| Gate Approved By | Who approved (`User` / `auto` for detection stages) |

**Audit value:** Proves each stage was reviewed and approved. Certification evidence.

### Session History

| Field | Purpose |
|-------|---------|
| Last Session | When the workflow was last active (enables "stale" detection) |
| Total Sessions | How many sessions this workflow has spanned |
| Session Platform | Which AI platform ran the last session |

---

## Package-Specific Fields

### AI-PILC (`pilc-state.md`) adds:

```markdown
## Input
- Source Type: structured-document
- Input Quality: high
- Source File: requirements_v2.docx

## Governance
- Pending Decisions: 2
- Register Counts: Decisions=6, Changes=1, Issues=3, Actions=4, Assumptions=5, Lessons=2
```

### AI-ADLC (`adlc-state.md`) adds:

```markdown
## Architecture
- Input Mode: Full PIP
- Enabled Extensions: [DDD Tactical, Resilience Patterns]
- Declined Extensions: [Microservices, BFF, Event Sourcing, Feature Flags]
- ADR Count: 8
- Architecture Workbook: 3 open items

## Containers
- Container Count: 4
- Components Designed: 12/16
```

### AI-GCE (`.compliance-state.json`) — different format:

```json
{
  "complianceTier": 2,
  "score": 87,
  "scoreHistory": [82, 83, 85, 86, 87],
  "lastAudit": "2026-06-12T14:30:00Z",
  "baselineDate": "2026-05-15",
  "baselineViolations": 47,
  "currentViolations": 15,
  "enforceFrom": "2026-05-15",
  "tierActivatedOn": {
    "tier1": "2026-05-15",
    "tier2": "2026-06-01",
    "tier3": null
  }
}
```

### AI-TGE (`tge-state.md`) adds:

```markdown
## Test Governance
- Mode: Full Chain
- Register Entries: 45
- Covered: 32
- Gaps: 13
- Risk Score (avg): 2.8/5
- Phase: Observation (Strategy complete)
```

---

## How Successor Packages Read State Files

| Successor | Fields It Reads | Why |
|-----------|----------------|-----|
| AI-ADLC reads `pilc-state.md` | Status, Depth, Output Structure, Project ID | Confirms PIP is complete, inherits depth, knows file naming |
| AI-DWG reads `adlc-state.md` | Enabled Extensions, Output Structure, Container Count | Triggers extension-enrichment, knows what to generate |
| AI-GCE reads workspace marker | (Doesn't read a state file — detects `.kiro/steering/`) | Presence = workspace exists |
| AI-TGE reads `adlc-state.md` | Extensions, ADR Count, Containers | Derives test requirements from architecture scope |

---

## How to Reconstruct a Lost State File

If state file is missing but artifacts exist:

```markdown
# {Package} State (Reconstructed)

## Project Identity
- Project ID: {from charter or first artifact header}
- Project Name: {from charter or PROJECT_INSTRUCTIONS.md}

## Progress
- Current Phase: {infer from last artifact — which phase does it belong to?}
- Current Stage: {count produced artifacts → last stage with artifact + 1}
- Status: {Complete if all artifacts exist, In Progress otherwise}
- Workflow Depth: {Standard (default) — or infer from artifact detail level}
- Output Structure: {look at filenames — numbered (01_, 02_) vs flat}

## Completed Stages
{List stages whose artifacts exist with estimated dates from file timestamps}
```

**This is sufficient for:**
- Resuming the workflow (position is correct)
- Successor detection (marker exists, status readable)

**What's lost:**
- Exact gate timestamps
- Decision log (if not in artifacts)
- Session history

---

## State File Location Rules

| Package Type | State File Location | Why There |
|-------------|--------------------|-----------| 
| Lifecycle (PILC, ADLC, POLC, UXD, ILC) | Root of output folder | Alongside the artifacts it tracks |
| Generator (DWG) | No state file — uses workspace marker | Generator output IS the workspace; marker is `workspace-rules.md` |
| Engine (GCE) | Workspace root (`.compliance-state.json`) | Governance applies to the whole workspace |
| Hybrid (TGE) | Root of test governance output | Alongside strategy + register |

---

## Related Documents

| Document | Location |
|----------|----------|
| How State Files Work | `knowledge_docs/HOW_STATE_FILES_WORK.md` |
| Pattern: Marker File Detection | `knowledge_docs/PATTERN_MARKER_FILE_DETECTION.md` |
| Pattern: Gate Before Transition | `knowledge_docs/PATTERN_GATE_BEFORE_TRANSITION.md` |
| What If State File Is Lost | `knowledge_docs/WHAT_IF_STATE_FILE_IS_LOST.md` |
| How Chain Handoff Works | `knowledge_docs/HOW_CHAIN_HANDOFF_WORKS.md` |

*Knowledge Document | Created: 2026-06-12 | Updated: 2026-06-13 | Author: [Mohammad Maheri](https://www.linkedin.com/in/mohammad-maheri-8399565b)*
