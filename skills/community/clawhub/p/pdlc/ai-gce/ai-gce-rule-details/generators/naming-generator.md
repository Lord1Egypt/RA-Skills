<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Naming Conventions — Derivation Logic

## Purpose

Derives naming convention rules (NC-*) from `naming-conventions.md`. 100% steering-derived — naming is entirely project-specific based on technology and team decisions.

---

## MANDATORY: Stage Sub-Role — Workspace Architect

During THIS activity, ALSO adopt the mindset of a **Workspace Architect**. This does NOT replace your primary role (Compliance Officer + Platform Engineer + AI-DLC v1 Engineer) — it ADDS a thinking dimension.

### Behavioral Shifts
- Think in consistency patterns: naming rules exist so that ANY file's purpose is immediately clear from its name
- Derive technology-specific patterns from the ACTUAL tech stack — NestJS uses `.controller.ts`, ASP.NET uses `Controller.cs`
- Cover all naming surfaces: files, folders, classes, methods, variables, URLs, database objects, test files
- Treat naming as foundational (Tier 1, Day 0): correct naming from the start prevents expensive renames later
- Ensure the naming-check hook uses module-specific patterns, not generic `**/*.ts`

### Anti-Patterns for This Activity
- Do NOT invent naming patterns beyond what naming-conventions.md states
- Do NOT mix naming rules with domain-language rules (NC-* is about FORMAT, DOM-* is about VOCABULARY)
- Do NOT use agentStop for naming if it causes false positives during intermediate refactoring states

### Quality Check
A good output from this activity sounds like:
- "NC-01: Controllers named `{Entity}Controller.ts` (NestJS). Derived from naming-conventions.md → File Naming. Hook pattern: `src/modules/*/presentation/**/*.controller.ts`. Tier 1."
- "naming-conventions.md covers 8 naming surfaces (files, folders, classes, methods, variables, URLs, tables, tests) → 8 NC-* rules generated."

---

## Source: `naming-conventions.md`

| Section to Extract | Generated Rules |
|-------------------|----------------|
| File naming patterns | NC-01: Controllers named `{Entity}Controller.{ext}` (per tech stack) |
| Folder naming (modules) | NC-02: Module folders follow stated pattern (kebab-case / PascalCase / etc.) |
| Class naming | NC-03: Classes follow stated pattern per layer |
| Method naming | NC-04: Methods follow stated convention |
| Variable naming | NC-05: Variables follow stated convention |
| API URL naming | NC-06: Endpoints follow stated URL pattern |
| Database naming (tables/columns) | NC-07: Tables/columns follow stated convention |
| Test file naming | NC-08: Test files follow stated pattern |

## Technology-Specific Pattern Table

The naming-check hook needs to know WHAT patterns to check based on the tech stack:

| Technology | Controller Pattern | Service Pattern | Entity Pattern |
|-----------|-------------------|----------------|---------------|
| NestJS | `{entity}.controller.ts` | `{entity}.service.ts` | `{entity}.entity.ts` |
| Django | `views.py` (module-level) | `services.py` | `models.py` |
| ASP.NET | `{Entity}Controller.cs` | `{Entity}Service.cs` | `{Entity}.cs` (in Entities/) |
| Spring Boot | `{Entity}Controller.java` | `{Entity}Service.java` | `{Entity}.java` (in entity/) |

## Hook: `naming-check.json`

- **Event:** agentStop (Tier B 🟡)
- **Pattern:** All source files in module paths
- **Checks:** NC-01 through NC-08 against all files modified in session

## Tier: 1 (naming is foundational — active from Day 0)
