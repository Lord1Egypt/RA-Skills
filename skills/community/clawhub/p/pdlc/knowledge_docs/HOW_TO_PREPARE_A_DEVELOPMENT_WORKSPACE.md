# How to Prepare a Development Workspace

**Purpose:** Practical guide for using AI-DWG to transform an Architecture Package into a ready-to-code development workspace — complete with steering files, governance structure, folder layout, and operational tooling that AI-DLC v1 (or any development workflow) consumes.

---

## Who This Is For

Tech leads, DevOps engineers, or senior developers setting up a project's development environment. You have architecture decisions made and need them translated into a workspace structure where the team can start building — with governance baked in from day one rather than bolted on later.

---

## Before You Start

**You need:**
- AI-DWG installed in your AI workspace (see `ai-dwg/setup/INSTALL.md`)
- **Required:** An Architecture Package (AP) from AI-ADLC — or equivalent architecture documents
- **Optional enrichment:**
  - Product Backlog Package (PBP) from AI-POLC
  - UX Design Package (UXP) from AI-UXD

**You do NOT need:**
- An existing codebase (unless brownfield — Mode 3)
- CI/CD already configured (AI-DWG generates templates)
- Team agreements written (AI-DWG generates those from architecture)

---

## Choosing Your Mode

AI-DWG operates in four modes depending on your situation:

| Mode | When to Use | What Happens |
|------|------------|-------------|
| **Mode 1: Full Generation** | New project, no existing workspace | Generates everything from scratch |
| **Mode 2: Delta Reconciliation** | Architecture changed after initial generation | Updates only affected files, preserves team edits |
| **Mode 3: Brownfield Overlay** | Existing codebase needs governance | Adds steering/hooks/governance WITHOUT touching existing code |
| **Mode 4: Extension Enrichment** | ADLC extension activated after workspace exists | Adds extension-specific steering rules to existing files |

**Most common:** Mode 1 for new projects. Mode 3 for teams adding governance to existing code.

---

## The Generation Process

### Mode 1: Full Generation (Step by Step)

**1. Input Detection**
- AI-DWG scans for `adlc-state.md` (AP marker)
- Optionally detects `polc-state.md` (PBP) and `uxd-state.md` (UXP)
- Reads enabled extensions from `adlc-state.md`

**2. Architecture Analysis**
- Extracts: containers, components, tech stack, API contracts, security model
- Maps container boundaries to folder structure
- Identifies which steering files are needed (conditional generation)

**3. Steering File Generation**
- Generates 19+ `.kiro/steering/` files from architecture decisions:

| Steering File | Derived From |
|--------------|-------------|
| `workspace-rules.md` | Overall architecture + methodology |
| `tech-stack.md` | Technology Stack decisions + ADRs |
| `api-standards.md` | API Architecture document |
| `security-rules.md` | Security Architecture |
| `module-structure.md` | Container/Component Architecture |
| `data-standards.md` | Data Architecture |
| `testing-strategy.md` | Quality requirements + architecture |
| `naming-conventions.md` | Tech stack conventions + team standards |
| `error-handling.md` | API + integration architecture |
| `logging-observability.md` | Non-functional requirements |
| `role-isolation.md` | Team structure + security architecture |
| `session-governance.md` | Methodology decisions |
| `project-governance.md` | Management framework + approach |
| ... | (conditional files based on architecture) |

**4. Workspace Structure Generation**
- Creates folder hierarchy matching container/component architecture
- Generates `PROJECT_INSTRUCTIONS.md` (project context for AI sessions)
- Creates `DEFINITION_OF_DONE.md`, `TEAM_AGREEMENTS.md`, `CODEOWNERS`
- Generates `docker-compose.yml` (if containerized architecture)
- Creates CI/CD templates matching chosen platform

**5. Governance Framework**
- Initializes `management_framework/` with registers
- Creates `MANAGEMENT_FRAMEWORK.md` linking all registers

**6. Review and Approve**
- AI-DWG presents the generated workspace for your review
- You approve, request changes, or reject individual files

---

## What You Get

```
{your-workspace}/
├── .kiro/
│   └── steering/                           ← 19+ steering files
│       ├── workspace-rules.md [marker]
│       ├── tech-stack.md
│       ├── api-standards.md
│       ├── security-rules.md
│       ├── module-structure.md
│       ├── data-standards.md
│       ├── testing-strategy.md
│       ├── naming-conventions.md
│       ├── error-handling.md
│       ├── logging-observability.md
│       ├── role-isolation.md
│       ├── session-governance.md
│       ├── project-governance.md
│       └── ... (conditional files)
├── PROJECT_INSTRUCTIONS.md                 ← Context for every AI session
├── DEFINITION_OF_DONE.md                   ← Quality criteria
├── TEAM_AGREEMENTS.md                      ← Team working standards
├── CODEOWNERS                              ← Code ownership mapping
├── docker-compose.yml                      ← Container orchestration (if applicable)
├── .github/ or .gitlab-ci/                 ← CI/CD templates
├── src/                                    ← Source structure matching architecture
│   ├── {container-1}/
│   │   ├── {component-a}/
│   │   └── {component-b}/
│   └── {container-2}/
│       └── ...
└── management_framework/                   ← Governance registers
    ├── MANAGEMENT_FRAMEWORK.md
    ├── Decision_Register.md
    ├── Change_Register.md
    ├── Issue_Register.md
    └── Lessons_Learned.md
```

---

## Conditional Generation

Not every file is generated for every project. AI-DWG uses triggers:

| Steering File | Generated When |
|--------------|---------------|
| `multi-tenancy.md` | AP contains multi-tenancy architecture |
| `event-sourcing.md` | Event Sourcing extension is active |
| `resilience-standards.md` | ≥3 external integrations OR Resilience extension active |
| `feature-flags.md` | Feature Flags extension is active |
| `frontend-standards.md` | AP contains frontend containers |
| `microservices.md` | Microservices extension is active |

If the architecture doesn't include these concerns, the files aren't generated — preventing bloat.

---

## Mode 3: Brownfield Overlay

For existing codebases, AI-DWG works differently:

1. **Scans existing workspace** — discovers current structure, existing configs, team conventions
2. **Generates governance only** — adds `.kiro/steering/`, `PROJECT_INSTRUCTIONS.md`, and operational docs
3. **Preserves everything** — zero changes to existing source code, configs, or team files
4. **Adapts to existing structure** — steering files reference actual folder paths, not idealized ones
5. **Flags gaps** — identifies where existing codebase diverges from architecture (for future reconciliation)

**Key principle:** Brownfield overlay is non-destructive. It ADDS governance alongside your existing code — it never moves, renames, or modifies what's already there.

---

## Tips for a Clean Generation

1. **Let extensions inform generation.** If AI-ADLC activated DDD Tactical, AI-DWG generates domain-specific folder structure and bounded-context steering. Don't disable extensions between packages.

2. **Review `workspace-rules.md` carefully.** This is the master steering file — it sets the tone for all AI sessions in the workspace. Ensure it reflects your team's actual working style.

3. **Customize `TEAM_AGREEMENTS.md` after generation.** AI-DWG seeds it from architecture decisions, but real team agreements need team input. Edit the generated file — it has `ownership: hybrid` and your edits are preserved on re-derivation.

4. **Don't skip `PROJECT_INSTRUCTIONS.md`.** This file gives every AI-DLC v1 session full project context. A rich project-instructions file means less repeated explanation in every chat session.

5. **Run Mode 2 when architecture changes.** If AI-ADLC revises an ADR or adds a container, run AI-DWG in Delta Reconciliation mode. It updates only affected steering files, preserving your customizations (the `<!-- custom -->` block pattern).

---

## What Happens Next

Your workspace feeds the final layer:

| Next Package | What It Reads |
|-------------|--------------|
| **AI-GCE** | All `.kiro/steering/` files → derives enforcement rules + hooks |
| **AI-TGE** | Testing steering + architecture → derives test governance |
| **AI-DLC v1** | Steering files + hooks + project instructions → builds with governance |

AI-GCE detects the workspace by finding `.kiro/steering/workspace-rules.md` (the marker).

---

## Related Documents

| Document | Location |
|----------|----------|
| How DWG Generation Engine Works | `knowledge_docs/HOW_DWG_GENERATION_ENGINE_WORKS.md` |
| How Chain Handoff Works | `knowledge_docs/HOW_CHAIN_HANDOFF_WORKS.md` |
| How to Run the Full Chain | `knowledge_docs/HOW_TO_RUN_THE_FULL_CHAIN.md` |
| How to Design Architecture | `knowledge_docs/HOW_TO_DESIGN_ARCHITECTURE.md` |
| Why Architecture Before Code Matters | `knowledge_docs/WHY_ARCHITECTURE_BEFORE_CODE_MATTERS.md` |

*Knowledge Document | Created: 2026-06-12 | Updated: 2026-06-13 | Author: [Mohammad Maheri](https://www.linkedin.com/in/mohammad-maheri-8399565b)*
