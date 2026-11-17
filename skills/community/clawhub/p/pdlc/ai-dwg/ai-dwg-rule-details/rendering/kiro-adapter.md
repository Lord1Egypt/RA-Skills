<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Kiro Adapter — Wire canonical `rules/` into `.kiro/steering/`

## Purpose

Renders the canonical `rules/` + reference folders into Kiro-native discovery: `.kiro/steering/` steering files (with `inclusion` front-matter), `.kiro/agents/` for workflows and governance, and `.kiro/hooks/` for lifecycle automation. Kiro is the **highest-capability** target — it supports all seven output categories natively.

**Load this file** during the rendering step when `platformTargets` includes `kiro`.

> **Canonical rule:** The actual rule text lives in `rules/*.md`. This adapter creates `.kiro/steering/` files that **reference** the canonical rules (via `#[[file:rules/...]]`) — it does NOT duplicate content. The one exception is the entry-point orchestrator, which Kiro requires as an always-loaded file.

---

## Category 1 — Entry Point

**Canonical source:** `rules/workspace-rules.md`

**Kiro wiring:** `.kiro/steering/workspace-rules.md` with `inclusion: auto` (always loaded). It carries the workspace identity + a reference to the canonical rules folder + the workspace-manifest pointer.

```markdown
---
inclusion: auto
---
<!-- Kiro adapter entry point — canonical rules in rules/ -->
# {Project Name} — Workspace Rules

Project ID: {projectId}
Canonical rules: `rules/` · Context map: `WORKSPACE_CONTEXT_MAP.md` · Manifest: `.governance/workspace-manifest.yaml`

#[[file:rules/workspace-rules.md]]
```

**Rule:** exactly ONE `inclusion: auto` steering file per workspace (the entry point).

---

## Category 2 — Scoped Rules

**Canonical source:** `rules/{concern}.md` (api-standards, security-rules, database-rules, design-system, etc.)

**Kiro wiring:** one `.kiro/steering/{concern}.md` per canonical rule, with `inclusion: fileMatch` + a `fileMatchPattern` derived from the concern's scope (from `tech-stack.md` + `module-structure.md`). Each references its canonical rule.

```markdown
---
inclusion: fileMatch
fileMatchPattern: 'src/api/**|**/*.controller.ts'
---
<!-- Kiro adapter — scoped rule; canonical content in rules/api-standards.md -->
#[[file:rules/api-standards.md]]
```

| Canonical rule | fileMatchPattern (derived) |
|----------------|----------------------------|
| `rules/api-standards.md` | api dirs + handler globs from tech-stack |
| `rules/database-rules.md` | data/repository/migration globs |
| `rules/security-rules.md` | `src/**` (global — security is always-on; use `inclusion: always` if preferred) |
| `rules/design-system.md` | UI dirs + `**/*.tsx`/`**/*.vue`/css globs |
| `rules/module-structure.md` | `src/modules/**` |

**Global-scope rules** (security, error-handling) MAY use `inclusion: always` instead of fileMatch when they must load on every file.

---

## Category 3 — Per-Module Context

**Canonical source:** `rules/` + `architecture/` module descriptions (from C4 L3)

**Kiro wiring:** Kiro has no native per-directory auto-load. Wire indirectly — the module context is captured in `rules/module-structure.md` (fileMatch-scoped to `src/modules/**`) and the orchestrator points to `architecture/` for deep lookup. Best-effort category on Kiro.

---

## Category 4 — Procedural Workflows

**Canonical source:** `rules/` + `info/` procedures (deploy, code-review, new-feature, reconcile)

**Kiro wiring:** `.kiro/agents/{workflow}.md` — one per procedure, invocable by the user. Each agent references its canonical procedure content.

---

## Category 5 — Governance Agents

**Canonical source:** `.governance/agents/*` (drift-detect, coverage, compliance — produced by GCE/TGE downstream)

**Kiro wiring:** `.kiro/agents/{check}.md` + registered `{XXX}__` shortcut in the entry-point steering. DWG installs the workspace-integrity agent (`WIA__`) here; GCE/TGE add their agents later. Full support.

> Note: DWG installs its own governance agent per `flows/agent-installation.md`. GCE and TGE install theirs downstream. All land in `.kiro/agents/` on Kiro.

---

## Category 6 — Automation Hooks

**Canonical source:** `.governance/` hook definitions

**Kiro wiring:** `.kiro/hooks/*.json` (event types: fileEdited, fileCreated, preToolUse, postToolUse, agentStop, etc.). Security-critical checks fire on `fileEdited` (immediate); advisory on `agentStop` (batch). Full native support — Kiro's event bus fires hooks automatically.

**Hook naming:** destination-workspace hooks are named per the generated project's convention (project name / concern), NOT the AIFLC build-workspace prefix. The `AIFLC ` name prefix is a build-workspace rule and does not apply to hooks DWG generates into a user's project.

---

## Category 7 — Discovery

**Canonical source:** `WORKSPACE_CONTEXT_MAP.md` (root) + `rules/relevance-map.md`

**Kiro wiring:** the entry-point orchestrator references the context map; `rules/relevance-map.md` is fileMatch-scoped so that when a developer works in `src/modules/{x}/`, the relevant `backlog/` stories + `ux/wireframes/` + `architecture/` refs auto-surface. This is Kiro's strength — fileMatch turns the relevance map into automatic context loading.

```markdown
---
inclusion: fileMatch
fileMatchPattern: 'src/modules/onboarding/**'
---
<!-- Auto-surface reference material for the onboarding module -->
When working here, consult:
- `backlog/epics/EPIC-001_stories/` (acceptance criteria)
- `ux/wireframes/WF-01_*.md` (screen specs)
- `ux/user-flows/UF-01_*.md` (interaction flow)
```

---

## Generated Kiro Layout

```
workspace/
├── rules/                          ← canonical (adapter references these)
├── .kiro/
│   ├── steering/
│   │   ├── workspace-rules.md      ← inclusion: auto (entry point)
│   │   ├── {concern}.md            ← inclusion: fileMatch → #[[file:rules/{concern}.md]]
│   │   └── {module}-context.md     ← inclusion: fileMatch → relevance-map surfacing
│   ├── agents/
│   │   ├── {workflow}.md           ← procedural workflows
│   │   └── {governance-check}.md   ← governance agents (WIA + GCE/TGE)
│   └── hooks/
│       └── *.json                  ← lifecycle automation
├── backlog/ ux/ architecture/ info/  ← reference (platform-neutral)
└── .governance/                    ← manifest, drift register, agent defs
```

---

## Kiro-Specific Advantages

- **Compaction-safe:** `inclusion: auto`/`fileMatch` steering is re-injected after context compaction
- **Native spec paradigm:** `.kiro/specs/` available (if build method is spec-driven — but that's a downstream choice, not DWG's concern)
- **Event-driven hooks:** fire automatically, no manual invocation
- **fileMatch = free relevance:** the relevance map becomes automatic context loading

---

## Output Validation

- [ ] Exactly one `inclusion: auto` steering file (entry point)
- [ ] Every scoped steering file references canonical `rules/` via `#[[file:...]]` (no duplicated content)
- [ ] fileMatch patterns derived from tech-stack + module-structure (never generic `**/*`)
- [ ] `.kiro/agents/` + `.kiro/hooks/` created for supported categories
- [ ] Relevance map wired via fileMatch for per-module context surfacing
- [ ] Entry point references `WORKSPACE_CONTEXT_MAP.md` + `.governance/workspace-manifest.yaml`
