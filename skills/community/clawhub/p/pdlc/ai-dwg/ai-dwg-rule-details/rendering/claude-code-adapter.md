<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Claude Code Adapter — Wire canonical `rules/` into `CLAUDE.md` + `.claude/`

## Purpose

Renders the canonical `rules/` + reference folders into Claude Code-native discovery: a root `CLAUDE.md` entry point (with `@import`), `.claude/rules/` with `paths:` frontmatter for auto-scoped loading, `.claude/skills/` for procedural workflows, `.claude/agents/` for isolated governance subagents, and `.claude/settings.json` for deterministic hooks. Claude Code is a **high-capability** target — it supports all seven categories, with context-efficiency advantages over Kiro (path-scoped auto-load vs. manual hashtag).

**Load this file** during the rendering step when `platformTargets` includes `claude-code`.

> **Canonical rule:** rule text lives in `rules/*.md`. This adapter's `.claude/rules/` files carry `paths:` frontmatter + an `@import` (or reference) to the canonical rule — they do NOT duplicate content. `CLAUDE.md` stays an index (<200 lines).

---

## Category 1 — Entry Point

**Canonical source:** `rules/workspace-rules.md`

**Claude Code wiring:** root `CLAUDE.md`, kept under 200 lines — an index/orchestrator that `@import`s the canonical entry point and points to the context map + manifest.

```markdown
<!-- Claude Code adapter entry point — canonical rules in rules/ -->
# {Project Name}

Project ID: {projectId}
Canonical rules: `rules/` · Context map: `WORKSPACE_CONTEXT_MAP.md` · Manifest: `.governance/workspace-manifest.yaml`

@import rules/workspace-rules.md

## How rules load
Scoped rules live in `.claude/rules/` (auto-loaded by path). Reference material: `backlog/`, `ux/`, `architecture/`. Workflows: `.claude/skills/`. Governance: `.claude/agents/`.
```

**Rule:** `CLAUDE.md` MUST stay under 200 lines — index only, never full rules. Every `@import` path MUST resolve.

---

## Category 2 — Scoped Rules

**Canonical source:** `rules/{concern}.md`

**Claude Code wiring:** one `.claude/rules/{concern}.md` per canonical rule, with `paths:` frontmatter (auto-scoped — Claude loads it only when touching matching files). Each references the canonical rule.

```markdown
---
paths: ["src/api/**", "**/*.handler.*"]
---
<!-- Claude Code adapter — scoped; canonical content in rules/api-standards.md -->
@import ../../rules/api-standards.md
```

| Canonical rule | `paths:` (derived) |
|----------------|--------------------|
| `rules/api-standards.md` | `["src/api/**", "**/*.controller.*", "**/*.handler.*"]` |
| `rules/database-rules.md` | `["src/data/**", "**/*repository*", "**/migrations/**"]` |
| `rules/security-rules.md` | `["src/**"]` (global — security always-on) |
| `rules/design-system.md` | `["src/ui/**", "**/*.tsx", "**/*.css", "**/*.scss"]` |
| `rules/module-structure.md` | `["src/modules/**"]` |

> **Advantage over Kiro:** `paths:` is automatic (no manual `#hashtag`), and rules are re-injected on compaction up to a shared budget. This gives better context efficiency — irrelevant rules never load.

---

## Category 3 — Per-Module Context

**Canonical source:** `architecture/` module descriptions (C4 L3) + relevant `rules/`

**Claude Code wiring:** `src/{module}/CLAUDE.md` — subdirectory context files that Claude auto-loads when working in that directory. Zero cost until the directory is touched. Each describes the module's bounded context + points to its `backlog/` stories + `ux/` specs.

```markdown
<!-- Per-module context for {module} — auto-loads when Claude works in src/{module}/ -->
# {Module} — Local Context
Bounded context: {from architecture/}. Key patterns: see `rules/module-structure.md`.
Build against: `backlog/epics/EPIC-{n}_stories/`. Screens: `ux/wireframes/WF-{n}_*.md`.
```

**Full native support** — this is a Claude Code strength (Kiro can only do this indirectly).

---

## Category 4 — Procedural Workflows

**Canonical source:** `rules/` + `info/` procedures

**Claude Code wiring:** `.claude/skills/{workflow}/SKILL.md` — invocable via `/command` or auto-match. One skill per procedure (deploy, code-review, new-feature, reconcile).

```markdown
---
name: deploy
description: Deployment checklist derived from architecture/technical-environment.md
---
# Deploy Skill
{procedure steps — references architecture/ + info/CICD_GUIDE.md}
```

---

## Category 5 — Governance Agents

**Canonical source:** `.governance/agents/*` (drift-detect, coverage, compliance)

**Claude Code wiring:** `.claude/agents/{check}/AGENT.md` — runs in an isolated context window, returns only a summary (doesn't pollute the main coding session). YAML frontmatter (name, description, optional model/tools).

```markdown
---
name: drift-detect
description: Measure workspace reality against the DWG baseline; report drift.
---
# Drift Detection Agent
{references .governance/baseline-manifest.yaml + drift-register.md}
```

**Full support** — subagent isolation is a Claude Code strength (governance checks cost zero main-session tokens).

---

## Category 6 — Automation Hooks

**Canonical source:** `.governance/` hook definitions

**Claude Code wiring:** `.claude/settings.json` hooks — `PreToolUse`, `PostToolUse`, `Stop`. `command`-type hooks are deterministic (can exit code 2 to hard-block); `agent`-type for advisory judgment.

```json
{
  "hooks": {
    "PreToolUse": [{ "matcher": "Write|Edit", "hooks": [{ "type": "command", "command": "{security-check-script}" }] }],
    "Stop": [{ "hooks": [{ "type": "agent", "agent": "drift-detect" }] }]
  }
}
```

**Full support** — deterministic (exit code 2 blocks), safer than prompt-following for security-critical checks.

---

## Category 7 — Discovery

**Canonical source:** `WORKSPACE_CONTEXT_MAP.md` + `rules/relevance-map.md`

**Claude Code wiring:** `CLAUDE.md` references the context map; per-module `src/{module}/CLAUDE.md` files surface the relevant `backlog/`/`ux/` material for that module (the relevance map, expressed as subdirectory context). Auto-loads on directory touch.

---

## Generated Claude Code Layout

```
workspace/
├── CLAUDE.md                       ← root entry point (<200 lines, @import rules/)
├── rules/                          ← canonical (adapter references these)
├── .claude/
│   ├── rules/
│   │   ├── {concern}.md            ← paths: [...] → @import ../../rules/{concern}.md
│   │   └── …
│   ├── skills/
│   │   └── {workflow}/SKILL.md     ← procedural workflows
│   ├── agents/
│   │   └── {check}/AGENT.md        ← isolated governance subagents
│   └── settings.json               ← hooks (PreToolUse/PostToolUse/Stop)
├── src/
│   └── {module}/CLAUDE.md          ← per-module context (auto-load on touch)
├── backlog/ ux/ architecture/ info/  ← reference (platform-neutral)
└── .governance/                    ← manifest, drift register, agent defs
```

---

## Claude Code-Specific Advantages (surface to user)

- **Path-scoped rules** derived from C4 boundaries — better context efficiency than always-loaded
- **Subagents in isolation** — governance without polluting the coding session
- **Skills as `/commands`** — lifecycle procedures invocable, derived from architecture
- **Deterministic hooks** — `PreToolUse` exit-code-2 hard-blocks (not prompt-following)
- **Subdirectory `CLAUDE.md`** — per-module context at zero cost until touched

---

## Output Validation

- [ ] `CLAUDE.md` at root, under 200 lines, index only
- [ ] Every `@import` path resolves to an existing canonical file
- [ ] `.claude/rules/*.md` carry `paths:` frontmatter + reference `rules/` (no duplicated content)
- [ ] `paths:` derived from tech-stack + module-structure (never generic)
- [ ] `.claude/skills/`, `.claude/agents/`, `settings.json` created for supported categories
- [ ] Per-module `src/{module}/CLAUDE.md` generated from C4 L3
- [ ] `CLAUDE.md` references `WORKSPACE_CONTEXT_MAP.md` + `.governance/workspace-manifest.yaml`
