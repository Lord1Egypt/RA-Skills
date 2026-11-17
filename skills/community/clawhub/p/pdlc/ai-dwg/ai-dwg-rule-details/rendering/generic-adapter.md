<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Generic Adapter — `rules/` Self-Sufficient + Universal Pointer

## Purpose

The fallback renderer for any platform without a dedicated adapter (or when the user wants a tool-neutral workspace). The canonical `rules/` + reference folders ARE already plain, readable markdown — any AI agent or human can read them directly. The Generic adapter adds a single human-and-agent-readable entry point and routes all enforcement to CI/CD. This is the **minimum viable** target — still valuable (architecture-derived structure + rules), just with no editor-level automation.

**Load this file** during the rendering step when `platformTargets` includes `generic` (or when a requested platform has no specific adapter).

> **Canonical rule:** Generic adds NO wiring layer that duplicates content. `rules/` is the source AND the delivery. The only new file is a top-level guide that points into `rules/` and the reference folders.

---

## Category 1 — Entry Point

**Canonical source:** `rules/workspace-rules.md`

**Generic wiring:** `WORKSPACE_GUIDE.md` at root — a human-and-agent-readable project guide. Points to `rules/`, the context map, and the reference folders. Not auto-loaded by any platform (no mechanism) — the user/agent opens it first by convention.

```markdown
<!-- Generic adapter entry point — tool-neutral -->
# {Project Name} — Workspace Guide

Project ID: {projectId}

## Start Here
1. Read `rules/workspace-rules.md` — the golden rules
2. Consult `rules/{concern}.md` for the area you're working in (see index below)
3. Reference material: `backlog/` (stories), `ux/` (screens/flows), `architecture/` (constraints/ADRs)
4. Context map: `WORKSPACE_CONTEXT_MAP.md` · Manifest: `.governance/workspace-manifest.yaml`

## Rules Index
| When working in | Read |
|-----------------|------|
| API code | `rules/api-standards.md` |
| Data/DB | `rules/database-rules.md` |
| Anywhere | `rules/security-rules.md` |
| UI | `rules/design-system.md` |
| Modules | `rules/module-structure.md` |
```

---

## Category 2 — Scoped Rules

**Native support:** ❌ No auto-loading on a generic platform.

**Generic wiring:** `rules/*.md` are flat, readable files. The `WORKSPACE_GUIDE.md` index maps area → rule. Loading is manual (human/agent opens the relevant file). No duplication — the guide points, `rules/` holds.

---

## Category 3 — Per-Module Context

**Native support:** ❌ None.

**Generic wiring:** `src/{module}/README.md` — human-readable per-module context (bounded context + pointers to backlog/ux). Read on demand.

---

## Category 4 — Procedural Workflows

**Generic wiring:** `docs/workflows/{procedure}.md` — readable playbooks (deploy, code-review, new-feature). Invoked manually.

---

## Category 5 — Governance Agents

**Native support:** ❌ None.

**Generic wiring:** `docs/governance/{check}.md` — manual-reference checks. Any automation lives in CI/CD (Category 6).

---

## Category 6 — Automation Hooks

**Native support:** ❌ None (no editor event system).

**Generic wiring:** `.github/workflows/*.yml` (or `scripts/` + a documented pipeline) — CI/CD is the ONLY enforcement layer on a generic platform. Lint, test, security scan, drift-check run in the pipeline.

---

## Category 7 — Discovery

**Canonical source:** `WORKSPACE_CONTEXT_MAP.md` + `rules/relevance-map.md`

**Generic wiring:** `WORKSPACE_GUIDE.md` links the context map; both are readable markdown any agent parses. The relevance map is a plain table (module → reference artifacts).

---

## Generated Generic Layout

```
workspace/
├── WORKSPACE_GUIDE.md              ← entry point (human + agent readable)
├── rules/                          ← canonical (IS the delivery — read directly)
├── docs/
│   ├── workflows/{procedure}.md    ← readable playbooks
│   └── governance/{check}.md       ← manual checks
├── .github/workflows/*.yml         ← CI/CD enforcement (the only automation)
├── src/{module}/README.md          ← per-module reference
├── backlog/ ux/ architecture/ info/  ← reference (platform-neutral)
├── .governance/                    ← manifest, drift register
├── WORKSPACE_CONTEXT_MAP.md        ← discovery index
└── PLATFORM_NOTES.md               ← discloses all editor-level automation is via CI/CD
```

---

## PLATFORM_NOTES.md (Generic)

```markdown
## Platform Capability Notice
Target: generic

✅ Full support: readable rules, reference material, discovery, structure — works with ANY agent
⚠️ Manual: rule loading (open the relevant rules/ file), workflows (readable playbooks)
❌ No editor automation: no scoped auto-load, no subagents, no editor hooks

ALL enforcement is CI/CD + human discipline. This is the tool-neutral baseline — every
other platform adapter builds richer wiring on top of the same canonical rules/.
```

---

## When Generic Is Used

- User selects `generic` explicitly (tool-neutral / mixed-tooling team)
- A requested platform has no dedicated adapter yet (safe fallback)
- Multi-target where one target is an unsupported/unknown platform

The Generic output is ALWAYS valid because it relies only on readable markdown + CI/CD — no platform features assumed.

---

## Output Validation

- [ ] `WORKSPACE_GUIDE.md` at root with rules index + reference pointers
- [ ] No content duplication — guide points, `rules/` holds
- [ ] `docs/workflows/`, `docs/governance/` readable playbooks
- [ ] CI/CD enforcement scaffold in `.github/workflows/` or `scripts/`
- [ ] `WORKSPACE_CONTEXT_MAP.md` + `.governance/workspace-manifest.yaml` present
- [ ] `PLATFORM_NOTES.md` states all automation is CI/CD-based
