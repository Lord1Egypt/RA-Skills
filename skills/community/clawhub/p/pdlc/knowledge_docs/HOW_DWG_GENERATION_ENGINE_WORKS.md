# How the AI-DWG Generation Engine Works

**Purpose:** Explains how AI-DWG reads an Architecture Package and transforms it into a ready-to-code development workspace — the internal mechanics of its mapping engine, conditional generation, extension awareness, and reconciliation mode.

---

## What AI-DWG Does

AI-DWG is a one-time generator that compiles architecture decisions into an operational development environment. It reads every artifact from AI-ADLC's Architecture Package and produces steering files, project structure, configuration, and operational documents — all populated with project-specific rules derived from architecture decisions.

```
ARCHITECTURE PACKAGE (from AI-ADLC)
├── Architecture Vision + Principles
├── System Context (C4 L1)
├── Container Diagram (C4 L2)
├── Technology Stack + ADRs
├── Security Architecture
├── Data Architecture
├── API Architecture
├── Integration Architecture
├── Infrastructure & Deployment
├── Component Design (C4 L3)
└── [Multi-Tenancy] [Extensions output]
        │
        ▼
┌─────────────────────────────────────────────────────────────┐
│  AI-DWG ENGINE                                               │
│                                                              │
│  READ → MAP → GENERATE → VALIDATE → OUTPUT                  │
│                                                              │
│  23 mapping files transform AP artifacts → workspace output  │
│  Conditional logic decides what to include/exclude           │
│  Extension detection enriches relevant files                 │
└─────────────────────────────────────────────────────────────┘
        │
        ▼
DEVELOPMENT WORKSPACE (ready for AI-DLC v1)
├── .kiro/steering/ (19+ steering files)
├── Operational docs (7 files)
├── Planning templates (3 files)
├── Config files (.gitignore, .editorconfig, docker-compose)
├── Source structure (from C4 L3 modules)
└── Management framework spine
```

---

## The Five-Step Generation Flow

### Step 1: READ — Load Architecture Package

The engine locates the AP via marker detection (`adlc-state.md`), then loads ALL artifacts:

- Parses each for: explicit decisions, constraints, patterns, technology labels, module names, quality attributes
- Checks `adlc-state.md` for: output structure (numbered/flat), enabled extensions, completion status
- Optionally detects PBP (`polc-state.md`) and UXP (`uxd-state.md`) for enrichment

**If a required artifact is missing:** Flag the gap to the user. Offer to generate with assumptions OR wait for the artifact.

### Step 2: MAP — Transform AP Artifacts → Workspace Artifacts

Each AP artifact maps to specific workspace output via 23 mapping rule files:

| AP Source | Mapping File | Produces |
|-----------|-------------|----------|
| Architecture Vision | `vision-to-workspace-rules.md` | `workspace-rules.md`, `architecture-principles.md` |
| Technology Stack | `techstack-to-config.md` | `tech-stack.md`, `.gitignore`, `.editorconfig`, `docker-compose.yml` |
| Component Design (C4 L3) | `components-to-structure.md` | Source folder layout |
| Component Design | `components-to-domain-context.md` | `domain-context.md` |
| Security Architecture | `security-to-steering.md` | `security-rules.md` |
| API Architecture | `api-to-steering.md` | `api-standards.md` |
| Data Architecture | `data-to-steering.md` | `database-rules.md` |
| Multi-Tenancy | `tenancy-to-steering.md` | `multi-tenancy.md` (conditional) |
| Infrastructure | `infra-to-config.md` | `docker-compose.yml` (enrichment) |
| Infrastructure | `infra-to-cicd.md` | `git-workflow.md`, CI/CD guide |
| Infrastructure | `infra-to-observability.md` | `observability-*.md` files |
| Integration | `integration-to-resilience.md` | `resilience-standards.md` (conditional) |
| Governance decisions | `governance-derivation.md` | `project-governance.md`, `session-governance.md`, `role-isolation.md` |
| Quality attributes | `quality-to-dod.md` | `DEFINITION_OF_DONE.md` |
| Team context | `team-to-agreements.md` | `TEAM_AGREEMENTS.md`, `CONTRIBUTING.md` |

### Step 3: GENERATE — Produce All Files

Files are generated using templates from `ai-dwg-rule-details/templates/`:
- **Steering files** (19 always + conditionals) → `.kiro/steering/`
- **Operational docs** (7 files) → project root
- **Planning templates** (3 files) → `templates/`
- **Config files** → project root
- **Folder structure** → `{src-structure}/`

**Critical rule:** Generated content is POPULATED — not placeholders. Steering files contain actual rules derived from AP decisions. The output is ready-to-use from day 1.

### Step 4: VALIDATE — Cross-Check Against AP

Verification ensures nothing was lost in translation:
- All AP principles encoded in at least one steering file
- All AP constraints reflected as MUST/NEVER rules
- Folder structure matches C4 L3 module decomposition
- Technology labels consistent across all files
- No contradictions between steering files
- Conditional files generated ONLY when AP justifies them

### Step 5: OUTPUT — Present Summary

Generation results are summarized: file counts, conditional files included/skipped, and next steps (run AI-GCE, begin AI-DLC v1).

---

## Three Operating Modes

| Mode | When | What Happens |
|------|------|-------------|
| **1. Full Generation** | No workspace exists yet | Complete generation from AP → all files produced |
| **2. Delta Reconciliation** | Architecture changed after initial generation | Diff → propose changes → user approves → merge preserving customizations → signal AI-GCE |
| **3. Brownfield Overlay** | Existing codebase needs governance layered on | Generate steering files + non-conflicting docs; skip source folders; merge configs additively |

### Delta Reconciliation (Mode 2) — Key Mechanics

When architecture changes after initial generation:

1. Read updated AP artifact(s) + current workspace state
2. Diff: identify what changed and which workspace files are affected
3. Propose specific changes (never auto-apply)
4. User approves per-file or in bulk
5. Merge preserving team customizations (`<!-- custom -->` markers)
6. Signal AI-GCE to re-derive affected rules

**Non-destructive guarantee:** Team-added content in steering files (marked `<!-- custom -->`) is always preserved during reconciliation.

### Brownfield Overlay (Mode 3) — Key Mechanics

For existing codebases that need governance:

| Category | Behavior |
|----------|----------|
| Steering files | Generate ALL (doesn't conflict with code) |
| Source folders | SKIP — code already exists |
| Config files | MERGE — add missing entries, preserve existing |
| Operational docs | Generate if missing; SKIP if exists (team's docs are sacrosanct) |

---

## Conditional Generation Logic

Not every project needs every file. AI-DWG generates conditional steering files only when the AP justifies them:

| Conditional File | Generated When |
|-----------------|----------------|
| `multi-tenancy.md` | AP contains Multi-Tenancy Architecture document |
| `api-versioning.md` | AP specifies multi-version API strategy |
| `resilience-standards.md` | System is distributed with >3 integrations OR Resilience extension active |
| `observability-tracing.md` | AP specifies distributed tracing tool OR Microservices extension active |
| `performance-standards.md` | AP defines latency SLOs |
| `workflow-engine.md` | AP describes workflow component |
| `frontend-standards.md` | AP has UI containers OR BFF extension active |
| `event-sourcing.md` | Event Sourcing extension was active in AI-ADLC |
| `feature-flags.md` | Feature Flags extension was active in AI-ADLC |
| `brownfield-patterns.md` | AP was produced in brownfield mode (Mode D) |

---

## Extension-Aware Generation

AI-DWG detects AI-ADLC v1.1 extensions from `adlc-state.md` and enriches generation:

| Active Extension | Enrichment Effect |
|-----------------|-------------------|
| DDD Tactical | Enriches `domain-context.md`, `module-structure.md`, `naming-conventions.md` with tactical patterns |
| Microservices | Forces `resilience-standards.md` + `observability-tracing.md` generation; enriches `module-structure.md` |
| BFF Pattern | Forces `frontend-standards.md` generation; enriches `api-standards.md` |
| Event Sourcing/CQRS | Generates `event-sourcing.md` steering; enriches `database-rules.md` |
| Resilience Patterns | Forces `resilience-standards.md` with full detail |
| Feature Flags | Generates `feature-flags.md` steering file |

**Rule:** Extensions OVERRIDE normal conditional triggers. If an extension was active, its outputs are generated regardless of the normal "number of integrations" or "latency SLO" triggers.

---

## Downstream Signal

After generation or reconciliation, AI-DWG signals AI-GCE:

```
⚡ DOWNSTREAM SIGNAL
   From: AI-DWG
   To: AI-GCE
   Event: {workspace-generated | steering-files-updated}
   Workspace root: {path}
   Steering files: .kiro/steering/ ({n} files)
   Action required: Derive compliance hooks from steering files
```

---

## Configuration Questions (Asked Once)

AI-DWG asks only 2-4 questions — everything else is derived from the AP:

| # | Question | Purpose |
|---|----------|---------|
| 1 | Workspace root path? | Where to generate |
| 2 | Project display name? | Used in README, PROJECT_INSTRUCTIONS |
| 3 | Team size (approximate)? | Affects operational doc depth |
| 4 | Target Kiro autonomy mode? | Influences session governance content |

Technology, architecture patterns, and folder structure are NOT asked — the AP already provides those answers.

---

## Related Documents

| Document | Location |
|----------|----------|
| Core generator | `ai-dwg/ai-dwg-rules/core-generator.md` |
| AP reading guide | `ai-dwg/ai-dwg-rule-details/common/ap-reading-guide.md` |
| Mapping files (23) | `ai-dwg/ai-dwg-rule-details/mapping/` |
| Reconciliation logic | `ai-dwg/ai-dwg-rule-details/reconciliation/` |
| Templates (48) | `ai-dwg/ai-dwg-rule-details/templates/` |
| Family Structure | `FAMILY_STRUCTURE.md` |

*Knowledge Document | Created: 2026-06-11 | Updated: 2026-06-13 | Author: [Mohammad Maheri](https://www.linkedin.com/in/mohammad-maheri-8399565b)*
