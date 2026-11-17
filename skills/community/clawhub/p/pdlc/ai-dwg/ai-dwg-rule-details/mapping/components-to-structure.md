<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Mapping: Component Design (C4 L3) → Folder Structure + CODEOWNERS + module-structure.md

## Purpose

This mapping rule transforms the **Component Design (C4 Level 3)** document into three workspace artifacts:
1. `{src-structure}/` — Physical folder layout reflecting module decomposition
2. `CODEOWNERS` — Ownership mapping per module/folder
3. `rules/module-structure.md` — Module boundaries, dependency rules, and layer conventions

---

## MANDATORY: Stage Sub-Role — Workspace Architect

During THIS activity, ALSO adopt the mindset of a **Workspace Architect**. This does NOT replace your primary role (DevOps/Platform Engineer + Senior Architect) — it ADDS a thinking dimension.

### Behavioral Shifts
- Make the architecture visible in the file system — folder structure IS the architecture diagram made tangible
- Think about day-1 developer experience: a new team member should understand module boundaries from folder names alone
- Encode dependency rules as enforceable constraints, not suggestions — module-structure.md feeds AI-GCE hooks
- Consider CODEOWNERS as a governance tool — ownership drives review quality and accountability
- Resist over-structuring — if the AP defines flat modules without layers, generate flat folders

### Anti-Patterns for This Activity
- Do NOT invent modules beyond what C4 L3 defines — folder structure = C4 L3, no more, no less
- Do NOT add internal layers (domain/, infrastructure/) unless the AP explicitly defines them
- Do NOT generate code files — AI-DWG creates structure only; code is AI-DLC v1's responsibility

### Quality Check
A good output from this activity sounds like:
- "Generated 8 module folders matching C4 L3 decomposition. Pattern A (layered) applied because AP defines domain/application/infrastructure layers. Shared kernel folder created per AP's cross-cutting component definition."
- "CODEOWNERS maps each module to team ownership from AP. Steering files assigned to @architect-team. Shared kernel requires broader review (cross-cutting impact)."

---

## Source (AP Artifact)

**Document:** Component Design (typically `11_Component_Diagram_C4L3.md` or `design/component-design.md`)

**Sections to extract:**

| Section | Contains | Maps To |
|---------|----------|---------|
| Module list per container | Named modules with responsibilities | Folder structure + module-structure.md |
| Module boundaries | What can depend on what | module-structure.md dependency rules |
| Dependency rules | Allowed/forbidden inter-module dependencies | module-structure.md |
| Shared kernel / shared components | Cross-cutting code shared between modules | Shared folder in structure |
| Interface contracts | Public APIs between modules | module-structure.md |
| Internal layer structure | Layers within each module (if defined) | Subfolder conventions |
| Component ownership | Team/person responsible per module | CODEOWNERS |
| Cross-cutting concerns | Logging, auth, error handling patterns | module-structure.md |

---

## Target 1: Folder Structure ({src-structure}/)

### Role

The physical directory layout that developers work in. It directly mirrors the architectural module decomposition — making the architecture visible in the file system.

### Generation Logic

```
FOR EACH container in C4 L2:
  IF container is the primary application:
    Create top-level src/ folder
    FOR EACH module in that container's C4 L3:
      Create module folder: src/{module-name}/
      IF internal layers defined:
        Create layer subfolders per convention
      
  IF container is a separate service (microservices):
    Create service folder: services/{service-name}/
    FOR EACH module in that service's C4 L3:
      Create module folder: services/{service-name}/src/{module-name}/

  IF shared kernel exists:
    Create: src/shared/ or libs/shared/
```

### Folder Naming Convention

| Architecture Term | Folder Name | Rule |
|------------------|-------------|------|
| Module / Bounded Context | `{kebab-case-name}/` | Lowercase, hyphenated |
| Shared Kernel | `shared/` or `common/` | Based on technology convention |
| Internal layer: Application/Use Cases | `application/` or `use-cases/` | Technology-specific |
| Internal layer: Domain | `domain/` | Universal |
| Internal layer: Infrastructure | `infrastructure/` | Universal |
| Internal layer: Presentation/API | `api/` or `controllers/` | Technology-specific |
| Internal layer: Ports | `ports/` | If hexagonal architecture |
| Internal layer: Adapters | `adapters/` | If hexagonal architecture |

### Structure Patterns (Based on Architecture Style)

**Pattern A: Modular Monolith (Feature-Based)**

```
src/
├── {module-1}/
│   ├── {module-1}.module.{ext}       ← Module entry point (framework-specific)
│   ├── application/                   ← Use cases / services
│   ├── domain/                        ← Entities, value objects, rules
│   ├── infrastructure/                ← Repos, external adapters
│   └── api/                           ← Controllers, DTOs
├── {module-2}/
│   ├── ...
├── {module-n}/
│   ├── ...
├── shared/                            ← Shared kernel (if exists)
│   ├── domain/                        ← Shared entities/interfaces
│   ├── infrastructure/                ← Shared utilities
│   └── types/                         ← Shared type definitions
└── main.{ext}                         ← Application entry point
```

**Pattern B: Microservices**

```
services/
├── {service-1}/
│   ├── src/
│   │   ├── {module-a}/
│   │   ├── {module-b}/
│   │   └── shared/
│   ├── package.json (or equivalent)
│   └── Dockerfile
├── {service-2}/
│   ├── src/
│   │   └── ...
│   └── Dockerfile
└── libs/                              ← Shared libraries across services
    ├── contracts/                     ← Shared DTOs, event schemas
    └── common/                        ← Shared utilities
```

**Pattern C: Simple (No Internal Layers)**

```
src/
├── {module-1}/
├── {module-2}/
├── {module-n}/
└── shared/
```

### Pattern Selection

| AP Indicates | Use Pattern |
|-------------|-------------|
| C4 L3 defines internal layers (domain, application, infrastructure) | Pattern A (layered modules) |
| C4 L2 has multiple application containers | Pattern B (microservices) |
| C4 L3 lists modules without internal structure | Pattern C (simple) |
| DDD Tactical extension active | Pattern A with domain/ emphasis |

### What Gets Created

For each module folder, create:
- The folder itself (empty — code is AI-DLC v1's job)
- A `.gitkeep` file (so empty folders are tracked in git)
- NO code files — AI-DWG generates structure, not code

---

## Target 2: CODEOWNERS

### Role

Maps file/folder paths to responsible owners. Used by git platforms (GitHub, GitLab, Bitbucket) to auto-assign reviewers and enforce ownership.

### Generation Logic

```
FOR EACH module in C4 L3:
  IF ownership is specified in AP (team/person per module):
    Map: /src/{module-name}/ → @{owner}
  ELSE:
    Map: /src/{module-name}/ → @{default-team}

IF shared kernel exists:
  Map: /src/shared/ → @{architecture-team or all}

ALWAYS include:
  /rules/ → @{architect or tech-lead}
  /CODEOWNERS → @{tech-lead}
```

### Structure

```
# ═══════════════════════════════════════════
# {Project Name} — Code Ownership
# Generated by AI-DWG | Source: Component Design (C4 L3)
#
# Format: <pattern> <owner>
# Owners are GitHub teams or usernames (adjust for your platform)
# ═══════════════════════════════════════════

# Governance & Architecture (requires architect review)
/rules/                @{architect-team}
/CODEOWNERS                     @{tech-lead}
/PROJECT_INSTRUCTIONS.md        @{tech-lead}
/DEFINITION_OF_DONE.md          @{tech-lead}

# Module ownership
/src/{module-1}/                @{owner-1}
/src/{module-2}/                @{owner-2}
/src/{module-n}/                @{owner-n}

# Shared kernel (requires broader review)
/src/shared/                    @{architect-team}

# Infrastructure & Config
/docker-compose.yml             @{devops-team}
/.github/                       @{tech-lead}
```

### Rules

1. Every module folder MUST have an owner
2. Shared kernel requires architect/tech-lead review (cross-cutting impact)
3. Steering files require architect review (architecture governance)
4. If AP doesn't specify owners → use `{team}` placeholder with comment: `# TODO: Assign team ownership`
5. Format follows platform convention (GitHub uses `@`, GitLab uses groups)

---

## Target 3: module-structure.md

### Role

Steering file that defines module boundaries, dependency rules, and internal conventions. This is the architectural constraint that prevents module coupling and boundary violations.

### Structure

```markdown
---
inclusion: always
---

<!-- AI-DWG generated | source: Component Design (C4 L3) | date: {generation-date} -->

# Module Structure

## Architecture Style

{monolith | modular-monolith | microservices} — {1-sentence description of the decomposition approach}

## Modules

<!-- begin: AP-sourced -->

| Module | Responsibility | Bounded Context | Owner |
|--------|---------------|-----------------|-------|
| `{module-1}` | {single responsibility — from AP} | {context name} | {owner} |
| `{module-2}` | {responsibility} | {context} | {owner} |
| ... | ... | ... | ... |
| `shared` | Cross-cutting utilities and shared contracts | Platform | {architect} |

<!-- end: AP-sourced -->

## Dependency Rules

<!-- begin: AP-sourced -->

### Allowed Dependencies

| From Module | Can Depend On | Reason |
|-------------|---------------|--------|
| `{module-a}` | `shared` | Shared kernel access |
| `{module-a}` | `{module-b}` (interface only) | {reason from AP} |
| Any module | `shared` | Universal shared kernel |

### Forbidden Dependencies

| From Module | MUST NOT Depend On | Reason |
|-------------|-------------------|--------|
| `{module-a}` | `{module-c}` (directly) | {reason — e.g., separate bounded contexts} |
| Any module | Another module's `domain/` internals | Encapsulation — use public interface only |
| Any module | Another module's `infrastructure/` | Implementation detail — never cross-reference |

<!-- end: AP-sourced -->

## Layer Rules (Within Each Module)

<!-- begin: AP-sourced -->

{Include ONLY if AP defines internal layers}

| Layer | Purpose | Can Reference | MUST NOT Reference |
|-------|---------|---------------|-------------------|
| `domain/` | Business logic, entities, rules | Nothing (innermost layer) | infrastructure/, api/, external libraries |
| `application/` | Use cases, orchestration | domain/ | infrastructure/ directly (use ports) |
| `infrastructure/` | External adapters (DB, API, queue) | domain/ (implements ports), application/ | Other module's infrastructure/ |
| `api/` | HTTP controllers, DTOs | application/ | domain/ directly, infrastructure/ directly |

**Dependency direction:** api/ → application/ → domain/ ← infrastructure/

<!-- end: AP-sourced -->

## Module Communication

<!-- begin: AP-sourced -->

| Pattern | When to Use | Mechanism |
|---------|------------|-----------|
| Direct import (interface) | Same bounded context, tight coupling acceptable | Import from module's public barrel file |
| Event / Message | Different bounded contexts, loose coupling required | {event bus / message queue — from AP} |
| API call | Cross-service (microservices only) | HTTP / gRPC — per api-standards.md |

<!-- end: AP-sourced -->

## Public Interface Convention

Every module exposes its public API through a single entry point:

```
src/{module-name}/
├── index.{ext}              ← Public barrel — ONLY export what other modules may use
├── {module-name}.module.{ext}  ← Module registration (framework-specific)
└── ...internal files...     ← NOT importable from outside
```

**Rules:**
1. Other modules MUST import from the barrel file (`index.{ext}`) — NEVER from internal paths
2. If it's not exported from the barrel → it's private to the module
3. Adding a new public export requires review (it's a contract change)

## Adding New Modules

When a new module is needed during development:

1. Verify it doesn't overlap with existing module responsibilities
2. Create folder following the established pattern
3. Update this file (add to Modules table + Dependency Rules)
4. Update CODEOWNERS with owner
5. If it crosses bounded contexts → requires ADR

## Anti-Patterns (DO NOT)

1. **DO NOT** create circular dependencies between modules
2. **DO NOT** import from another module's internal paths (bypass barrel)
3. **DO NOT** put business logic in shared/ — shared is for contracts and utilities only
4. **DO NOT** create "god modules" that everything depends on (except shared kernel)
5. **DO NOT** duplicate code between modules instead of extracting to shared (if truly shared)
6. **DO NOT** bypass the layer rules — no controller calling a repository directly
```

### Transformation Rules

| AP Content | Transformation | Output |
|-----------|---------------|--------|
| Module list with responsibilities | Copy to Modules table | Module registry |
| "Module A depends on Module B" | Add to Allowed Dependencies | Dependency whitelist |
| "Module A must not access Module B" | Add to Forbidden Dependencies | Dependency blacklist |
| Internal layer descriptions | Convert to Layer Rules table | Layer dependency matrix |
| Inter-module communication patterns | Map to Communication section | Integration patterns |
| Shared kernel definition | Add as `shared` module with special rules | Module table + dependency rules |

---

## Key Rules for This Mapping

1. **Folder structure = C4 L3 — no more, no less.** Don't invent modules; don't omit modules.
2. **Empty folders are fine.** AI-DWG creates structure; AI-DLC v1 writes code. Folders with only `.gitkeep` are expected.
3. **Dependency rules are BLOCKING.** They become enforceable constraints for AI-GCE.
4. **Layer rules only if AP specifies them.** If C4 L3 doesn't define internal structure, use Pattern C (flat modules).
5. **CODEOWNERS uses placeholders** if AP doesn't specify teams. Comment with `# TODO: Assign team ownership`.
6. **module-structure.md is the most enforcement-heavy steering file.** It defines what AI-GCE will check on every PR.
7. **Shared kernel is restrictive.** Adding to shared/ requires broader review because it affects all modules.

---

## Depth Adaptation

| Depth | Folder Structure | CODEOWNERS | module-structure.md |
|-------|-----------------|------------|-------------------|
| **Minimal** | Flat module folders (Pattern C) | Module-level ownership only | Module table + basic dependency list |
| **Standard** | Layered modules (Pattern A) with standard layers | Module + shared + config ownership | Full structure as defined above |
| **Comprehensive** | Layered modules + sub-module folders + per-feature structure | Granular ownership (per subfolder) | Full + sequence diagrams for key inter-module flows + DDD boundary analysis |

---

## Reconciliation Behavior

When Component Design changes:

| Change | Impact | Action |
|--------|--------|--------|
| New module added | New folder, CODEOWNERS entry, module-structure row | Add all three; flag for team awareness |
| Module renamed | Folder rename, CODEOWNERS update, module-structure update | Propose rename — DO NOT auto-rename (may have code) |
| Module removed | Flag for user | NEVER auto-delete — module may have code; user decides |
| Dependency rule added | module-structure.md update | Add rule; signal AI-GCE to enforce |
| Dependency rule removed | module-structure.md update | Remove rule; warn that previously-blocked code may now be allowed |
| Module split into two | New folders, CODEOWNERS entries, dependency rules | Propose the split; user confirms before creating |
| Shared kernel changed | shared/ folder impact, broad CODEOWNERS scope | Flag HIGH IMPACT — affects all modules |
