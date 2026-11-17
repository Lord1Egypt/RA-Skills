# How AI-DWG Brownfield Detection Works

**Purpose:** Explains how AI-DWG's Mode 3 (Brownfield Overlay) detects an existing codebase's structure, conventions, and governance gaps — then generates governance artifacts that integrate non-destructively alongside what already exists.

---

## What Brownfield Detection Is

When AI-DWG encounters an existing codebase instead of an empty workspace, it switches to Brownfield Overlay mode. Instead of generating everything from scratch, it scans what exists, maps the current reality, identifies governance gaps, and overlays steering/governance WITHOUT modifying existing source code.

```
EXISTING CODEBASE
├── src/ (team's code — UNTOUCHED)
├── package.json (team's config — UNTOUCHED)
├── .eslintrc (team's linting — UNTOUCHED)
└── README.md (team's docs — UNTOUCHED)
        │
        ▼
┌─────────────────────────────────────────────────────────────────────┐
│  AI-DWG BROWNFIELD DETECTION (Mode 3)                                │
│                                                                      │
│  SCAN         →    MAP          →    GAP ANALYSIS   →   OVERLAY      │
│  (discover       (build model     (what governance    (add .kiro/    │
│   what exists)    of current)      is missing?)        steering/)    │
└─────────────────────────────────────────────────────────────────────┘
        │
        ▼
EXISTING CODEBASE + GOVERNANCE OVERLAY
├── src/ (UNCHANGED)
├── package.json (UNCHANGED)
├── .kiro/steering/ (NEW — generated from scan + AP)
├── PROJECT_INSTRUCTIONS.md (NEW)
├── DEFINITION_OF_DONE.md (NEW)
└── management_framework/ (NEW)
```

**Core guarantee:** Brownfield detection is read-only on existing files. It ADDS governance alongside; it NEVER modifies, moves, or renames existing artifacts.

---

## The Detection Process (4 Phases)

### Phase 1: Workspace Scan

AI-DWG scans the existing workspace to build a structural model:

| What's Scanned | What's Extracted |
|---------------|-----------------|
| Folder structure | Module/component boundaries, nesting patterns |
| Package files (`package.json`, `pom.xml`, `Cargo.toml`) | Tech stack, dependencies, scripts |
| Configuration files (`.eslintrc`, `tsconfig.json`, etc.) | Existing conventions, rule sets |
| CI/CD files (`.github/workflows/`, `Jenkinsfile`) | Existing automation, deploy patterns |
| Test directories | Test framework, folder pattern, naming convention |
| README / docs | Project description, existing architectural notes |
| Git history metadata | Active contributors, change frequency by module |
| Existing `.kiro/` folder | Prior governance (partial or full) |

### Phase 2: Convention Mapping

From the scan, AI-DWG builds a **Convention Model** — what patterns the team already follows:

```
Convention Model (derived from scan):
├── Language: TypeScript
├── Framework: Express.js
├── Module Pattern: feature-based folders (src/users/, src/orders/)
├── Test Pattern: co-located (__tests__/ inside each module)
├── Naming: kebab-case files, PascalCase classes
├── Linting: ESLint with Airbnb preset
├── CI: GitHub Actions (build + test on PR)
├── Coverage: Jest with 70% threshold (existing config)
└── Structure Depth: 2 levels (src/{feature}/{file})
```

**Key principle:** The convention model describes WHAT IS, not what should be. Steering files will reference the actual structure — not an idealized one.

### Phase 3: Gap Analysis

AI-DWG compares the existing workspace against the Architecture Package (if provided) or against universal governance requirements:

| Gap Category | Detection Method | Example Finding |
|-------------|-----------------|-----------------|
| Missing steering | No `.kiro/steering/` exists | "No governance steering files found" |
| Missing project context | No `PROJECT_INSTRUCTIONS.md` | "AI sessions have no project context" |
| Missing DoD | No quality gate document | "Definition of Done not documented" |
| Missing team agreements | No explicit working norms | "TEAM_AGREEMENTS.md absent" |
| Partial governance | Some steering exists but gaps | "tech-stack.md exists, api-standards.md missing" |
| Convention-steering mismatch | Config says X, no steering enforces X | "ESLint enforces naming but no naming steering" |
| Architecture-code drift | AP defines boundaries not reflected in code | "AP says 3 services; code has 5 folders" |

### Phase 4: Overlay Generation

Based on gaps identified, AI-DWG generates ONLY what's missing:

| Condition | Action |
|-----------|--------|
| No `.kiro/steering/` at all | Generate full steering set (adapted to scanned conventions) |
| Partial steering exists | Generate only missing files, leave existing untouched |
| Full steering exists but outdated | Flag as recommendation (don't overwrite) |
| Existing conventions not in steering | Generate steering that CODIFIES existing conventions |
| AP defines boundaries not in steering | Generate boundary steering referencing actual folders |

---

## How Steering Files Adapt to Existing Code

In greenfield (Mode 1), steering files reference idealized architecture. In brownfield (Mode 3), they reference the ACTUAL codebase:

**Greenfield `module-structure.md`:**
```markdown
## Module Boundaries
Modules MUST follow the container architecture defined in AP Section 3.
```

**Brownfield `module-structure.md`:**
```markdown
## Module Boundaries
Based on existing structure scan:
- `src/users/` — User domain (17 files, 4 contributors)
- `src/orders/` — Order domain (23 files, 3 contributors)
- `src/shared/` — Shared utilities (used by both domains)

Dependencies MUST flow: users → shared, orders → shared.
Cross-domain imports (users → orders, orders → users) are PROHIBITED.
```

The brownfield version is grounded in reality — making governance immediately enforceable.

---

## Architecture Package + Existing Code (Hybrid Mode)

When BOTH an AP and existing code are present:

1. **Scan existing code** → build Convention Model
2. **Read AP** → extract architectural intent
3. **Compare** → find alignment and drift

| AP Says | Code Shows | Action |
|---------|-----------|--------|
| 3 containers | 3 matching folders | Aligned — generate steering confirming boundaries |
| REST API with versioning | REST endpoints, no versioning | Drift — generate API steering noting gap, recommend versioning |
| PostgreSQL | PostgreSQL (in docker-compose) | Aligned — generate data steering matching config |
| Microservices | Monolithic structure | Major drift — flag in gap report, generate steering for current state with migration notes |

**Resolution rule:** Steering files govern the codebase AS IT IS, with explicit notes where architecture intent differs from current state. AI-GCE then enforces on new code toward the architectural intent.

---

## Non-Destructive Guarantees

| Guarantee | Mechanism |
|-----------|-----------|
| No source code changes | Brownfield mode writes only to `.kiro/`, `PROJECT_INSTRUCTIONS.md`, and governance folders |
| No config overwrite | Existing `.eslintrc`, `tsconfig.json`, etc. are READ (for convention detection) but never WRITTEN |
| No folder restructure | Existing folder hierarchy remains as-is; steering references actual paths |
| No dependency changes | `package.json` / `pom.xml` / etc. are read-only inputs |
| No git history impact | Only new files added; no force-pushes, no rebases |
| Existing `.kiro/` preserved | If partial governance exists, existing files are kept; only gaps are filled |

---

## Output Differences: Greenfield vs. Brownfield

| Artifact | Greenfield (Mode 1) | Brownfield (Mode 3) |
|----------|--------------------|--------------------|
| `workspace-rules.md` | From AP only | From AP + scanned conventions |
| `module-structure.md` | From AP containers/components | From actual folder structure + AP alignment |
| `tech-stack.md` | From AP technology decisions | From scanned dependencies + AP validation |
| `naming-conventions.md` | From AP + tech stack defaults | From detected existing patterns |
| `testing-strategy.md` | From AP quality requirements | From existing test setup + AP requirements |
| Folder structure | Generated from architecture | NOT generated (already exists) |
| CI/CD templates | Generated fresh | NOT generated (existing CI preserved) |
| `PROJECT_INSTRUCTIONS.md` | From AP context | From AP context + scanned project state |

---

## Downstream Impact

After brownfield overlay:
- **AI-GCE** reads the brownfield-aware steering and uses the baseline pattern (enforce forward, baseline existing)
- **AI-TGE** detects existing tests during its brownfield assessment stage and maps them against architectural requirements
- **AI-DLC v1** sessions get full project context via `PROJECT_INSTRUCTIONS.md` (grounded in actual codebase state)

---

## Related Documents

| Document | Location |
|----------|----------|
| How DWG Generation Engine Works | `knowledge_docs/HOW_DWG_GENERATION_ENGINE_WORKS.md` |
| How to Retrofit Governance on Existing Code | `knowledge_docs/HOW_TO_RETROFIT_GOVERNANCE_ON_EXISTING_CODE.md` |
| How to Prepare a Development Workspace | `knowledge_docs/HOW_TO_PREPARE_A_DEVELOPMENT_WORKSPACE.md` |
| Why Brownfield Awareness Matters | `knowledge_docs/WHY_BROWNFIELD_AWARENESS_MATTERS.md` |
| How Chain Handoff Works | `knowledge_docs/HOW_CHAIN_HANDOFF_WORKS.md` |

*Knowledge Document | Created: 2026-06-12 | Updated: 2026-06-13 | Author: [Mohammad Maheri](https://www.linkedin.com/in/mohammad-maheri-8399565b)*
