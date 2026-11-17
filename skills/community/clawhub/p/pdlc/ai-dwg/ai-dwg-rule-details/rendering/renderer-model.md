<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Renderer Model — Canonical `rules/` + Platform Adapters

## Purpose

This file defines HOW AI-DWG turns its platform-neutral canonical output into platform-native workspaces. DWG's shared core produces canonical content once; a **renderer** (one per selected platform) wires that content into the platform's native discovery mechanism. This is the abstraction that makes DWG **AI-agnostic** — the intelligence is generated once, packaged N ways.

**Load this file** at the start of the rendering step (after mapping/generation produces canonical content, before writing platform-specific files).

---

## MANDATORY: Stage Sub-Role — Workspace Architect + Automation Engineer

During rendering, ALSO adopt the **Workspace Architect** mindset (folder topology, discovery mechanics) layered with **Automation Engineer** (platform wiring, adapters). ADDS a dimension — does NOT replace the primary DevOps/Platform Engineer role.

### Behavioral Shifts
- Think "one source, N packagings" — never author content in an adapter; adapters only wire
- Respect each platform's native idiom — a Kiro user expects `.kiro/steering/`, a Cursor user expects `.cursor/rules/`
- Optimize for the platform's context-loading model — scoped where the platform supports it, compiled where it doesn't
- Disclose degradation honestly — if a platform can't do hooks, say so; don't fake it

### Anti-Patterns
- Do NOT copy rule content into an adapter file — adapters reference/include the canonical `rules/`
- Do NOT generate platform features the target doesn't support (no fake hooks for Cursor)
- Do NOT omit the canonical `rules/` — it is ALWAYS generated, even for a single platform target

---

## The Canonical + Adapter Model

```
DWG Shared Core (mapping rules → canonical content)
        │
        ▼
   rules/               ← CANONICAL (platform-neutral markdown) — ALWAYS generated
   backlog/ ux/ architecture/ info/   ← reference material (platform-neutral)
        │
        ├──▶ Kiro adapter        → .kiro/steering/     (rendering/kiro-adapter.md)
        ├──▶ Claude Code adapter → CLAUDE.md + .claude/ (rendering/claude-code-adapter.md)
        ├──▶ Cursor adapter      → .cursor/rules/       (rendering/cursor-adapter.md)
        ├──▶ Codex adapter       → AGENTS.md            (rendering/codex-adapter.md)
        └──▶ Generic             → rules/ self-sufficient (rendering/generic-adapter.md)
```

**Core invariant:** `rules/` (and the reference folders) hold the actual content. Adapters are **thin wiring** — they tell the platform's AI *where to look* and *when to load*, pointing back at the canonical files. No adapter ever contains original rule text.

---

## The Seven Output Categories

Every renderer MUST handle these seven categories. HOW each is expressed varies by platform; WHAT it contains is canonical.

| # | Category | Canonical Source | What the adapter does |
|---|----------|------------------|-----------------------|
| 1 | **Entry point** | `rules/workspace-rules.md` | Wire the always-loaded root instruction the AI reads first |
| 2 | **Scoped rules** | `rules/*.md` (per concern) | Wire conditional loading (by file-glob / path / hashtag) |
| 3 | **Per-module context** | `rules/` + `architecture/` module info | Wire per-directory context loading (if platform supports) |
| 4 | **Procedural workflows** | `rules/` + `info/` procedures | Wire invocable workflows (skills / agents / docs) |
| 5 | **Governance agents** | `.governance/agents/*` | Wire isolated governance checks (if platform supports) |
| 6 | **Automation hooks** | `.governance/` hook defs | Wire lifecycle automation (if platform supports) |
| 7 | **Discovery** | `WORKSPACE_CONTEXT_MAP.md` + `rules/relevance-map.md` | Wire the AI to the context map so it finds `backlog/`, `ux/`, `architecture/` |

Categories 3, 5, 6 are **best-effort** — platforms without the capability degrade to documentation + CI/CD (disclosed in `PLATFORM_NOTES.md`). Categories 1, 2, 4, 7 are **mandatory** on every platform.

---

## Capability Matrix (Drives Adapter Behavior)

| Category | Kiro | Claude Code | Cursor | Codex | Generic |
|----------|:----:|:-----------:|:------:|:-----:|:-------:|
| 1. Entry point | ✅ auto | ✅ auto | ✅ auto | ✅ auto | ⚠️ manual |
| 2. Scoped rules | ✅ fileMatch | ✅ paths | ⚠️ glob | ❌ sections | ❌ flat |
| 3. Per-module context | ⚠️ indirect | ✅ subdir | ❌ | ❌ | ⚠️ README |
| 4. Workflows | ✅ agents | ✅ skills | ⚠️ docs | ⚠️ docs | ⚠️ docs |
| 5. Governance agents | ✅ | ✅ subagent | ❌ | ❌ | ❌ |
| 6. Hooks | ✅ | ✅ | ❌ | ❌ | ⚠️ CI/CD |
| 7. Discovery | ✅ | ✅ | ✅ | ✅ | ✅ |

✅ native · ⚠️ degraded/manual · ❌ not supported (falls back to docs + CI/CD)

---

## Multi-Target Rendering

When the Config Gate Q2 returns **multiple** platforms:

1. Generate canonical `rules/` + reference folders ONCE
2. For EACH selected platform: run its adapter → write platform-native wiring
3. All adapters point at the SAME canonical `rules/`
4. Result: one workspace, one source of truth, N platform entry points side by side

Example (targets = `[kiro, claude-code]`):
```
workspace/
├── rules/                    ← canonical (shared by both adapters)
├── .kiro/steering/           ← Kiro adapter → references rules/
└── CLAUDE.md + .claude/      ← Claude adapter → @imports rules/
```

Both AIs work in the same workspace, reading the same canonical rules through their native mechanisms.

---

## Limited Platforms — Compiled Single File

Some platforms support only ONE always-loaded instruction file (e.g., Copilot's `.github/copilot-instructions.md`, Cline's `.clinerules`). For these, the adapter **compiles** the canonical `rules/` into one concatenated file:

1. Concatenate all applicable `rules/*.md` into the single file (in priority order)
2. Prepend the entry point (`workspace-rules.md`) content
3. Append pointers to `backlog/`, `ux/`, `architecture/` for reference lookup
4. Note in `PLATFORM_NOTES.md` that scoped loading is unavailable (everything always-loaded)

Compilation is the fallback ONLY for platforms with no multi-file discovery. Rich platforms always reference, never compile.

---

## Platform Capability Disclosure (`PLATFORM_NOTES.md`)

For any target below full capability, the adapter generates `PLATFORM_NOTES.md` in the workspace root disclosing what is degraded:

```markdown
## Platform Capability Notice

Targets: {platformTargets}

✅ Full support: {categories the platform handles natively}
⚠️ Degraded: {categories that fall back to docs/CI}
❌ Not supported: {categories with no equivalent — how they're handled instead}
```

Honesty over illusion — the user knows exactly what governance is automatic vs. manual on their platform.

---

## Rendering Step (Where This Fits in the Flow)

```
Mode 1 Full Generation:
  ... mapping produces canonical rules/ + backlog/ + ux/ + architecture/ + info/ ...
  ↓
  RENDERING STEP (this model):
    1. Read platformTargets from Config Gate Q2
    2. FOR EACH target: load rendering/{platform}-adapter.md → write native wiring
    3. Generate PLATFORM_NOTES.md if any target is below full capability
    4. Record platformTargets in workspace-manifest.yaml
  ↓
  ... validation + output summary ...
```

---

## Adapter File Index

| Platform | Adapter Detail File |
|----------|---------------------|
| Kiro | `rendering/kiro-adapter.md` |
| Claude Code | `rendering/claude-code-adapter.md` |
| Cursor | `rendering/cursor-adapter.md` |
| Codex | `rendering/codex-adapter.md` |
| Generic | `rendering/generic-adapter.md` |

Load the adapter file(s) for the selected target(s) during the rendering step.

---

## Output Validation

- [ ] Canonical `rules/` generated regardless of platform count
- [ ] One adapter run per selected platform
- [ ] No adapter contains original rule content (all reference `rules/`)
- [ ] `PLATFORM_NOTES.md` generated for any below-full-capability target
- [ ] `platformTargets` recorded in `workspace-manifest.yaml`
- [ ] Multi-target: all adapters point at the same canonical `rules/`
