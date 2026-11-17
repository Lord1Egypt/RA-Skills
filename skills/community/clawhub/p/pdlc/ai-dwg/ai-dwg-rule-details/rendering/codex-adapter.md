<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Codex Adapter — Wire canonical `rules/` into `AGENTS.md`

## Purpose

Renders the canonical `rules/` + reference folders into Codex-native discovery: a root `AGENTS.md` always-loaded instruction file with sectioned references to the canonical rules. Codex is a **lower-capability** target — it supports an always-loaded entry point and sectioned rules, but has **no native scoped-loading, subagent, hook, or per-directory model**. Those categories degrade to advisory docs + CI/CD, disclosed in `PLATFORM_NOTES.md`.

**Load this file** during the rendering step when `platformTargets` includes `codex`.

> **Canonical rule:** `AGENTS.md` references the canonical `rules/` by pointer + concise section summaries. Full rule text stays in `rules/`. `AGENTS.md` stays lean (pointers, not full copies) so it doesn't bloat the always-loaded context.

---

## Category 1 — Entry Point

**Canonical source:** `rules/workspace-rules.md`

**Codex wiring:** root `AGENTS.md` (always loaded by Codex). Carries workspace identity + a section index pointing to canonical rules + context map + manifest.

```markdown
<!-- Codex adapter entry point — canonical rules in rules/ -->
# {Project Name} — Agent Instructions

Project ID: {projectId}
Canonical rules: `rules/` · Context map: `WORKSPACE_CONTEXT_MAP.md` · Manifest: `.governance/workspace-manifest.yaml`

Read `rules/workspace-rules.md` first. Scoped rules are indexed below — consult the
matching `rules/{concern}.md` when working in the relevant area.
```

---

## Category 2 — Scoped Rules

**Native support:** ⚠️ Partial. No auto-scoping — Codex loads `AGENTS.md` wholesale.

**Codex wiring:** section index in `AGENTS.md` — one line per concern with its scope + a pointer to the canonical rule. Codex reads the pointer and opens the rule when relevant.

```markdown
## Rules Index (consult the file when working in the area)

| When working in | Read this rule |
|-----------------|----------------|
| `src/api/**`, `*.controller.*` | `rules/api-standards.md` |
| `src/data/**`, `**/migrations/**` | `rules/database-rules.md` |
| anywhere (security is global) | `rules/security-rules.md` |
| `src/ui/**`, `*.tsx`, `*.css` | `rules/design-system.md` |
| `src/modules/**` | `rules/module-structure.md` |
```

> **Degradation:** no automatic loading — the index tells Codex which rule to open. Full content stays in `rules/` to keep `AGENTS.md` lean.

---

## Category 3 — Per-Module Context

**Native support:** ❌ None.

**Degradation:** `src/{module}/README.md` for reference; the `AGENTS.md` rules index covers module scoping by glob pointer. Disclosed.

---

## Category 4 — Procedural Workflows

**Native support:** ⚠️ Partial. No native invocation.

**Degradation:** `docs/workflows/{procedure}.md` referenced from `AGENTS.md`; user invokes manually. Disclosed.

---

## Category 5 — Governance Agents

**Native support:** ❌ None.

**Degradation:** `docs/governance/{check}.md` — advisory playbooks; enforcement via CI/CD. Disclosed.

---

## Category 6 — Automation Hooks

**Native support:** ❌ None.

**Degradation:** `.github/workflows/*.yml` / `scripts/` — CI/CD enforcement. Disclosed.

---

## Category 7 — Discovery

**Canonical source:** `WORKSPACE_CONTEXT_MAP.md` + `rules/relevance-map.md`

**Codex wiring:** `AGENTS.md` references the context map and includes the relevance map as a section ("when working in module X, consult backlog/ + ux/"). Codex reads it as part of the always-loaded instructions.

---

## Generated Codex Layout

```
workspace/
├── AGENTS.md                       ← root entry point (always loaded; pointers + index)
├── rules/                          ← canonical (AGENTS.md points here)
├── docs/
│   ├── workflows/{procedure}.md    ← manual playbooks (Cat 4 degraded)
│   └── governance/{check}.md       ← advisory checks (Cat 5 degraded)
├── .github/workflows/*.yml         ← CI/CD enforcement (Cat 6 degraded)
├── src/{module}/README.md          ← per-module reference (Cat 3 degraded)
├── backlog/ ux/ architecture/ info/  ← reference (platform-neutral)
├── .governance/                    ← manifest, drift register
└── PLATFORM_NOTES.md               ← discloses Cat 2/3/5/6 degradation
```

---

## PLATFORM_NOTES.md (Codex)

```markdown
## Platform Capability Notice
Target: codex

✅ Full support: entry point (AGENTS.md), discovery
⚠️ Degraded: scoped rules (index-pointer, not auto-scoped), workflows (manual playbooks)
❌ Not supported: per-module auto-load, governance subagents (→ docs/), automation hooks (→ CI/CD)

Enforcement on Codex is advisory + CI/CD. Rules load via the AGENTS.md index — open the
referenced rules/ file when working in the matching area.
```

---

## Output Validation

- [ ] `AGENTS.md` at root, lean (pointers + index, not full rule copies)
- [ ] Rules index maps scope → canonical `rules/{concern}.md`
- [ ] Cat 3/5/6 degraded to docs/ + CI/CD, disclosed
- [ ] Entry point references context map + manifest
- [ ] `PLATFORM_NOTES.md` generated
