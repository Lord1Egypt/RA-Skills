# How Chain Handoff Works

**Purpose:** Explains how AI-* Family packages hand off to each other — the detection mechanism, marker files, contract structure, and signal flow that enable packages to run independently yet compose into a seamless pipeline.

---

## What Chain Handoff Means

The AI-* Family is a pipeline where each package produces output that feeds the next. Chain handoff is the mechanism that makes this work: each package publishes a marker file, defines what it produces, and its successor knows exactly what to look for and where to find it.

```
AI-ILC (optional)       AI-PILC              AI-ADLC              AI-DWG              AI-GCE
─────────────────       ───────              ───────              ───────              ───────
Marker: ilc-state.md    Marker: pilc-state.md   Marker: adlc-state.md   Marker: workspace-rules.md   Marker: .kiro/hooks/
        │                       │                       │                       │
        └───── reads ──────────►│                       │                       │
                                └───── reads ──────────►│                       │
                                                        └───── reads ──────────►│
                                                                                └─── signal ──►
                                                                                        (AI-DLC v1)
```

---

## The Three Principles

### 1. Detection by Marker, Not by Path

Packages find their predecessor's output by looking for a **marker file** — a non-negotiable filename that identifies the output. They do NOT look for a specific folder path.

| Package Output | Marker File |
|---------------|-------------|
| AI-ILC | `ilc-state.md` |
| AI-PILC | `pilc-state.md` |
| AI-ADLC | `adlc-state.md` |
| AI-DWG | `.kiro/steering/workspace-rules.md` |
| AI-GCE | `.kiro/hooks/` folder with at least one `.json` hook file |
| Shared governance spine | `management_framework/MANAGEMENT_FRAMEWORK.md` |

**Why markers:** Users choose WHERE output goes. A team might put their architecture docs in `./docs/arch/` or `./architecture/` or even a sibling repo. The marker lets the next package find it regardless of path.

**Detection strategy (all packages follow this pattern):**
1. User provides path explicitly → use it
2. Scan common locations for the marker
3. Not found → ask user: "Where is the {predecessor} output?"

### 2. User Owns WHERE, Package Defines WHAT

The user decides folder locations. The package defines:
- Which marker file must exist
- Which output files are guaranteed
- Which state fields successors need

This separation ensures packages work across any folder structure, drive, or even separate repositories.

### 3. Graceful Standalone (OR-Input Pattern)

Every package in the chain works without its predecessor. If the predecessor's output isn't detected, the package falls back to accepting raw input directly:

| Package | With Predecessor | Without Predecessor |
|---------|-----------------|---------------------|
| AI-PILC | Reads AI-ILC Idea Brief | Accepts raw requirements in any format |
| AI-ADLC | Reads PIP from AI-PILC | Accepts requirements + charter directly |
| AI-DWG | Reads AP from AI-ADLC | Accepts any structured architecture docs |
| AI-GCE | Reads workspace from AI-DWG | Reads any workspace with `.kiro/steering/` |

This means users can enter the chain at any point — not just the beginning.

---

## How a Handoff Works (Step by Step)

### Example: AI-PILC → AI-POLC

**1. AI-PILC completes and produces:**
- `pilc-state.md` (marker — contains project ID, status, depth, output structure)
- 12+ PIP artifacts (requirements, feasibility, charter, scope, risk, etc.)

**2. AI-POLC starts and runs detection:**
```
Scan for pilc-state.md:
  → ./project-initiation/pilc-state.md ← FOUND
```

**3. AI-POLC reads state file fields:**
- `Project ID: PRJ-ACME-2026-001` → Carried forward into `polc-state.md`
- `Status: Complete` → Full PIP handoff confirmed
- `Workflow Depth: Standard` → Indicates content richness
- `Output Structure: numbered` → Tells POLC which naming pattern to expect

**4. AI-POLC reads guaranteed output files:**
- Project Charter → extracts objectives, scope, constraints
- Scope Statement → extracts boundaries, WBS for epic decomposition
- Risk Register → inherits delivery risks
- Stakeholder Register → inherits stakeholder landscape for prioritization

**5. AI-POLC adapts its behavior:**
- Full PIP available → minimal questions needed (most context already captured)
- Depth inherited → POLC calibrates to same depth level

---

## The Contract Structure

Every package in the chain has a "Chain Contract" section in its core file defining:

### I Read (Predecessor)

| Field | Purpose |
|-------|---------|
| Predecessor name | Which package's output to look for |
| Marker file | The filename to detect |
| Detection strategy | How to find it (explicit → scan → ask) |
| Required fields | What state file fields must exist |
| What to read | Specific files/data consumed from predecessor output |
| Graceful degradation | What happens if predecessor output is absent |

### I Produce (Successor)

| Field | Purpose |
|-------|---------|
| Successor name | Who consumes this package's output |
| Marker file | What this package's marker is |
| Output location | Where output goes (user-chosen) |
| Guaranteed files | Files that the successor can depend on existing |
| State file fields | Data the successor reads from the marker |
| Signal format | How this package notifies downstream (if applicable) |

---

## Downstream Signaling

When a generator/engine updates workspace files that a downstream package depends on, it signals the successor to re-derive:

```
⚡ DOWNSTREAM SIGNAL
   From: AI-DWG
   To: AI-GCE
   Event: steering-files-updated
   Affected files: [list of changed steering files]
   Action required: Re-derive rules for changed files
```

| Source | Signals | When |
|--------|---------|------|
| AI-DWG | AI-GCE | After generation or reconciliation (steering files changed) |
| AI-ADLC | AI-DWG | After architecture change (AP artifact updated) |
| AI-PILC | — (no signal) | PIP is a one-time handoff; no reconciliation |

---

## Multi-Input Convergence (AI-DWG)

AI-DWG is unique: it reads from THREE parallel predecessors:

| Input | Producer | Required? | Marker |
|-------|----------|:---------:|--------|
| Architecture Package | AI-ADLC | ✅ Required | `adlc-state.md` |
| Product Backlog Package | AI-POLC | ⚪ Optional | `polc-state.md` |
| UX Design Package | AI-UXD | ⚪ Optional | `uxd-state.md` |

AP is the generation core. PBP and UXP are additive enrichment — when present they sharpen specific outputs, when absent the generator proceeds with no loss of core function.

---

## The Project ID — Family-Wide Correlation Key

AI-PILC mints a **Project ID** (`PRJ-{ABBREV}-{YYYY}-{NNN}`) at Stage 1 that follows the project through the entire chain:

```
AI-PILC mints: PRJ-ACME-2026-001
    → pilc-state.md carries it
    → AI-ADLC reads it, copies to adlc-state.md
    → AI-DWG reads it, embeds in PROJECT_INSTRUCTIONS.md
    → AI-PPM uses it for portfolio roll-up
    → AI-FLO uses it for routing decisions
```

This ID enables:
- Cross-package traceability (follow an initiative through the pipeline)
- Portfolio management (AI-PPM groups by project ID)
- Audit trail (all governance events tagged to one project)

---

## Format Tolerance

Packages support multiple output structures from their predecessors:

| Structure | Example | Supported By |
|-----------|---------|--------------|
| Numbered | `01_Architecture_Vision.md` | All successor packages |
| Phase-folder | `foundation/architecture-vision.md` | All successor packages |
| Flat | `pilc-docs/inception/*.md` | All successor packages |
| Custom | Any user-chosen layout | Via marker detection |

Detection uses filename patterns (`*Architecture_Vision*`) rather than exact paths, making it structure-agnostic.

---

## Cross-Repo Support

Predecessor output can be in a completely different location:
- Different folder on the same drive
- Different drive
- Different repository (checked out locally)
- A shared network path

As long as the marker file can be found, the chain works. The user provides the path, and the successor package scans from there.

---

## Related Documents

| Document | Location |
|----------|----------|
| AI-PILC chain contract | `ai-pilc/ai-pilc-rules/core-workflow.md` (§ Chain Contract) |
| AI-ADLC chain contract | `ai-adlc/ai-adlc-rules/core-workflow.md` (§ Chain Contract) |
| AI-DWG chain contract | `ai-dwg/ai-dwg-rules/core-generator.md` (§ Chain Contract) |
| AI-GCE chain contract | `ai-gce/ai-gce-rules/core-generator.md` (§ Chain Contract) |
| Family Structure | `FAMILY_STRUCTURE.md` |
| Naming & Ownership | `contracts/NAMING_AND_OWNERSHIP.md` |

*Knowledge Document | Created: 2026-06-11 | Updated: 2026-06-13 | Author: [Mohammad Maheri](https://www.linkedin.com/in/mohammad-maheri-8399565b)*
