<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Cursor Adapter — Wire canonical `rules/` into `.cursor/rules/`

## Purpose

Renders the canonical `rules/` + reference folders into Cursor-native discovery: `.cursor/rules/*.mdc` (with glob-based `globs:` frontmatter) or a root `.cursorrules` fallback. Cursor is a **medium-capability** target — it supports entry point, scoped rules (by glob), and discovery, but has **no native subagent, hook, or per-directory model**. Those categories degrade to advisory docs + CI/CD, disclosed in `PLATFORM_NOTES.md`.

**Load this file** during the rendering step when `platformTargets` includes `cursor`.

> **Canonical rule:** `.cursor/rules/*.mdc` files carry glob scoping + reference the canonical `rules/`. Content stays in `rules/`. For older Cursor versions that only support a single `.cursorrules`, the adapter **compiles** from `rules/` (see limited-platform path).

---

## Category 1 — Entry Point

**Canonical source:** `rules/workspace-rules.md`

**Cursor wiring (modern, `.cursor/rules/`):** an always-applied rule file:

```mdc
---
description: Workspace entry point
alwaysApply: true
---
<!-- Cursor adapter entry point — canonical rules in rules/ -->
Project ID: {projectId}. Canonical rules: rules/. Context map: WORKSPACE_CONTEXT_MAP.md.
See rules/workspace-rules.md for full workspace rules.
```

**Cursor wiring (legacy, single `.cursorrules`):** compiled — see limited-platform section.

---

## Category 2 — Scoped Rules

**Canonical source:** `rules/{concern}.md`

**Cursor wiring:** one `.cursor/rules/{concern}.mdc` per canonical rule, with `globs:` frontmatter (Cursor auto-applies when a matching file is in context). References the canonical rule.

```mdc
---
description: API standards
globs: ["src/api/**", "**/*.controller.*"]
---
<!-- Cursor adapter — scoped; canonical content in rules/api-standards.md -->
See rules/api-standards.md for full rules. Key points:
{brief pointer — full content stays in rules/}
```

| Canonical rule | `globs:` (derived) |
|----------------|--------------------|
| `rules/api-standards.md` | `["src/api/**", "**/*.controller.*"]` |
| `rules/database-rules.md` | `["src/data/**", "**/migrations/**"]` |
| `rules/security-rules.md` | `["src/**"]` (or `alwaysApply: true`) |
| `rules/design-system.md` | `["src/ui/**", "**/*.tsx", "**/*.css"]` |

> **Degradation vs Kiro/Claude:** Cursor's glob scoping works but there's higher context-budget pressure. DWG references `rules/` and keeps the `.mdc` files as thin pointers, not full copies.

---

## Category 3 — Per-Module Context

**Native support:** ❌ None. Cursor has no per-directory auto-load.

**Degradation:** folded into glob-scoped rules (`globs: ["src/modules/{x}/**"]`) OR `src/{module}/README.md` for human reference. Disclosed in `PLATFORM_NOTES.md`.

---

## Category 4 — Procedural Workflows

**Native support:** ⚠️ Partial. No native `/command` invocation.

**Degradation:** `docs/workflows/{procedure}.md` — reference playbooks the user invokes manually (paste or `@file`). Disclosed as manual.

---

## Category 5 — Governance Agents

**Native support:** ❌ None. No subagent/isolation model.

**Degradation:** `docs/governance/{check}.md` — advisory playbooks the user runs manually. Any enforcement moves to CI/CD (Category 6). Disclosed in `PLATFORM_NOTES.md`.

---

## Category 6 — Automation Hooks

**Native support:** ❌ None. No lifecycle event system.

**Degradation:** `.github/workflows/*.yml` or `scripts/` — CI/CD-based enforcement (lint, security scan, drift-check-on-CI). Deterministic at the pipeline level, not the editor level. Disclosed.

---

## Category 7 — Discovery

**Canonical source:** `WORKSPACE_CONTEXT_MAP.md` + `rules/relevance-map.md`

**Cursor wiring:** the entry-point rule references the context map; the relevance map is expressed as glob-scoped `.cursor/rules/` entries (`globs: ["src/modules/{x}/**"]` → "consult backlog/ + ux/ for this module"). Works via Cursor's glob mechanism.

---

## Limited-Platform Path (Legacy `.cursorrules`)

If the user's Cursor version supports only a single `.cursorrules` file (no `.cursor/rules/` folder):

1. Compile canonical `rules/*.md` into one `.cursorrules` (priority order: entry point → security → core → conditional)
2. Append pointers to `backlog/`, `ux/`, `architecture/` for reference lookup
3. Note in `PLATFORM_NOTES.md`: "scoped loading unavailable — all rules always-loaded; high context usage"

DWG detects version capability from user input at Config Gate (or generates both `.cursor/rules/` AND `.cursorrules`, letting Cursor pick).

---

## Generated Cursor Layout

```
workspace/
├── rules/                          ← canonical (adapter references these)
├── .cursor/
│   └── rules/
│       ├── workspace-rules.mdc     ← alwaysApply: true (entry point)
│       ├── {concern}.mdc           ← globs: [...] → pointer to rules/{concern}.md
│       └── {module}.mdc            ← globs: relevance-map surfacing
├── .cursorrules                    ← (legacy fallback — compiled, only if needed)
├── docs/
│   ├── workflows/{procedure}.md    ← manual playbooks (Cat 4 degraded)
│   └── governance/{check}.md       ← advisory checks (Cat 5 degraded)
├── .github/workflows/*.yml         ← CI/CD enforcement (Cat 6 degraded)
├── backlog/ ux/ architecture/ info/  ← reference (platform-neutral)
├── .governance/                    ← manifest, drift register
└── PLATFORM_NOTES.md               ← discloses Cat 3/5/6 degradation
```

---

## PLATFORM_NOTES.md (Cursor)

```markdown
## Platform Capability Notice
Target: cursor

✅ Full support: entry point, scoped rules (glob), discovery
⚠️ Degraded: workflows (manual playbooks in docs/), per-module context (folded into glob rules)
❌ Not supported: governance subagents (→ docs/governance/ manual), automation hooks (→ CI/CD scripts)

Enforcement on Cursor is advisory + CI/CD, not editor-level automatic.
```

---

## Output Validation

- [ ] `.cursor/rules/*.mdc` with `globs:`/`alwaysApply:` referencing canonical `rules/` (thin pointers, not copies)
- [ ] globs derived from tech-stack + module-structure
- [ ] Cat 3/5/6 degraded to docs/ + CI/CD, disclosed in `PLATFORM_NOTES.md`
- [ ] Legacy `.cursorrules` compiled only if version requires it
- [ ] Entry point references context map + manifest
- [ ] `PLATFORM_NOTES.md` generated
