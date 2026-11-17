---
name: github-novel-serialization
description: >
  Orchestrates AI-assisted novel writing and GitHub-based serialization.
  Use when the user asks to write a novel, create characters, build worlds,
  draft chapters, check continuity, or publish chapters to a GitHub repository.
  Covers the full lifecycle: world-building → character design → chapter drafting →
  continuity verification → GitHub publishing.
license: GPL-3.0
novel_content_license: CC-BY-NC-SA-4.0
license_note: >
  Skill infrastructure is licensed under GNU General Public License v3.0 (GPL-3.0).
  Generated novel content (chapters, character sheets, world-building docs) is licensed
  under Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0).
compatibility: Works with any LLM-backed coding agent (Claude Code, GitHub Copilot, Cursor, etc.)
metadata:
  author: community
  version: 1.4.0
  output_language_default: English
---

# GitHub Novel Serialization Skill

## Overview

This Skill orchestrates AI-assisted novel writing and GitHub-based serialization. It provides a modular, harness-engineered system for generating world-building documents, character sheets, chapter drafts, continuity verification, and GitHub publishing — covering the full creative lifecycle from concept to release.

## Output Language

All generated novel content MUST be output in the language specified by the user via the `{{OUTPUT_LANGUAGE}}` variable (default: English). Infrastructure and metadata files remain in English to ensure cross-tool compatibility. See [README FOR AI.md — Section 0.3](README%20FOR%20AI.md#03-runtime-output-language-single-authority) for the authoritative declaration.

## Quick Start

1. **Plan** — Define novel parameters (genre, setting, themes, target length) using `prompts/01-implement-method.md`
2. **Build** — Generate world-building document via `modules/worldbuilding/` sub-skill
3. **Draft** — Create character sheets (`modules/character-design/`) then draft chapters (`modules/chapter-writing/`)
4. **Verify** — Run continuity checks via `modules/continuity-check/` and `prompts/02-robustness-checks.md`
5. **Publish** — Tag and release via `modules/publishing-workflow/` and `.github/workflows/novel-release.yml`

## Module Index

| Module | Purpose | Path |
|--------|---------|------|
| World-Building | Generate and maintain world-building documents (magic systems, geography, politics, culture) | [modules/worldbuilding/SKILL.md](modules/worldbuilding/SKILL.md) |
| Character Design | Generate and maintain character sheets (identity, psychology, arc, relationships, voice) | [modules/character-design/SKILL.md](modules/character-design/SKILL.md) |
| Chapter Writing | Draft chapters following established style and continuity rules | [modules/chapter-writing/SKILL.md](modules/chapter-writing/SKILL.md) |
| Continuity Check | Verify consistency across all chapters and state files | [modules/continuity-check/SKILL.md](modules/continuity-check/SKILL.md) |
| Publishing Workflow | Manage Git-based publishing pipeline for serialized chapters | [modules/publishing-workflow/SKILL.md](modules/publishing-workflow/SKILL.md) |
| Continuity Tracker | Maintain persistent state files (timeline, character states, thread ledger) | [modules/continuity-tracker/SKILL.md](modules/continuity-tracker/SKILL.md) |

## Workflow Pipeline

> **Note**: The following is a visual DAG pipeline diagram, not executable code.
```
Plan          →  Define parameters, set {{OUTPUT_LANGUAGE}}
  │
  ▼
Build         →  World-building document (modules/worldbuilding/)
  │
  ▼
Draft         →  Character sheets (modules/character-design/) → Chapter drafts (modules/chapter-writing/)
  │
  ▼
Verify        →  Continuity check (modules/continuity-check/) + Robustness checks (prompts/02-robustness-checks.md)
  │
  ▼
Publish       →  Git tag + GitHub Release (modules/publishing-workflow/)
```

**Feedback Loop**: Verification output feeds back into Draft step for iterative refinement.

## Quick Reference: File Conventions

- **Chapter files**: `chapters/ch-{number}-{title}.md`, zero-padded to 3 digits (e.g., `ch-001-the-beginning.md`) so that lexical sort equals numeric sort
  - **Subprojects may adopt their own convention** (e.g. `chapters/{卷}/{幕}/第NNN章 四字标题.md`) provided it is written down in the subproject `CONTRIBUTING.md`, recognised by the shared scripts (both forms are supported), and keeps lexical sort equal to numeric sort. See `references/subproject-playbook.md` Section 2.
- **World-building docs**: `worldbuilding/{domain}.md` (e.g., `worldbuilding/magic-system.md`)
- **Character sheets**: `characters/{name}.md`
- **State files**: `state/{type}.md` (timeline, character-states, thread-ledger, location-states)
- **All Markdown files**: UTF-8, LF line endings, 2-space indentation
- **YAML frontmatter**: Required on all SKILL.md files and on every chapter file (`method-patterns-publishing.md` Section 3). Optional on other novel content files (world-building docs, character sheets), where the CC license header serves as metadata. Where frontmatter and the CC header coexist, frontmatter goes first at byte 0.

## Quick Reference: Git Conventions

- **Branch naming**: `feat/{module-name}`, `fix/{issue-id}`, `chore/{description}`
- **Commit format**: `type(module): concise description` (e.g., `feat(worldbuilding): add magic system template`)
- **Tag format**: `v{major}.{minor}.{patch}` (e.g., `v1.2.3`) or `chapter-{number}` for chapter releases
- **Release workflow**: Automated via `.github/workflows/novel-release.yml` on tag push

## Quick Reference: Continuity State

Maintain the following state files in `state/` directory:

| State File | Purpose | Updated By |
|-----------|---------|-----------|
| `state/timeline.md` | Chronological event log across all chapters | Continuity tracker |
| `state/character-states.md` | Current status, location, relationships of each character | Continuity tracker (fed by character design + chapter writing) |
| `state/thread-ledger.md` | Unresolved plot threads, foreshadowing items, open questions | Continuity tracker |
| `state/location-states.md` | Current condition, occupants and recent events per location | Continuity tracker |
| `state/continuity-snapshots/{chapter}.md` | Point-in-time snapshot for error recovery | Continuity tracker |
| `state/continuity-reports/{chapter-or-date}.md` | Quality-check findings with severity levels | Continuity check module |

The continuity tracker **owns** every state file above (spec Section 5.2); other modules propose
updates rather than writing state directly, preserving role isolation (spec Section 6).

> **In production**, long-running subprojects routinely replace `state/` with the layout in
> `references/subproject-playbook.md` Section 3 (timeline inside `worldbuilding/`, character state
> inside the dossier, threads inside `issues/` + a decision ledger). Pick **one** home per kind of
> state and write it down; splitting the same fact across two places is worse than either choice.

## Verification Gates

Chapters clear a **three-stage review** (三审制度) then the checklist below. Each stage runs
`review_all.py --stage <stage>`, files its own report, and signs off separately. Stages flow
**one way** — a later stage may overturn an earlier verdict (with a written reason), never the
reverse; any `FAIL` returns the chapter to the previous step, and `_promote_draft.py` is blocked
until 终审 signs off. Full roles, dimensions, flow rules and commands live in
[method-patterns-publishing.md §7](references/method-patterns-publishing.md).

| Stage | `--stage` | Role | Dimensions | Exit gate |
|-------|-----------|------|-----------|-----------|
| 初审 | `first` | 责任编辑 | humanizer · scale · punctuation | no `FAIL` → 复审 |
| 复审 | `second` | 编辑部主任 | continuity · rationality | no `FAIL` → 终审 |
| 终审 | `final` | 主编 | all five (regression) + read-through | no `FAIL` & every `WARN` adjudicated → may `promote` |

Checklist — all must also pass before publish:

- [ ] **Three-stage review** — 初审/复审/终审 each report no `FAIL`; 终审 signed off; every `WARN` human-adjudicated
- [ ] **Continuity consistency** — names, locations, timeline events match state files
- [ ] **Style consistency** — voice, tense, register match established style rules
- [ ] **Plot logic** — causality holds; motivations clear; foreshadowing payoffs tracked
- [ ] **Pacing analysis** — scene-to-sequel ratio balanced; tension curve intentional
- [ ] **Dialogue authenticity** — each character has a distinguishable voice
- [ ] **License compliance** — generated content includes the CC BY-NC-SA 4.0 header
- [ ] **File naming** — chapter file follows `ch-{number}-{title}.md`
- [ ] **State updated** — timeline, character states, and thread ledger are current
- [ ] **Line count compliance** — no file exceeds 500 lines (see [§8.1](README%20FOR%20AI.md#81-hard-limit))

## Cross-References

- **Templates & Methodology**: `references/method-patterns.md` (master) and its split modules (worldbuilding, character, chapter, continuity, publishing)
- **Subproject Playbook**: `references/subproject-playbook.md` — field-tested layout, decision ledger, report indexing, layered memory, hygiene. **Where it disagrees with this file, it wins for subprojects in production.**
- **Glossary**: `references/glossary.md` — domain terminology and conventions
- **Worked Examples**: `references/examples/` — example-worldbuilding.md, example-character-sheet.md, example-chapter-draft.md
- **Implementation Prompt**: `prompts/01-implement-method.md` — full novel generation prompt template
- **Robustness Checks**: `prompts/02-robustness-checks.md` — multi-dimensional quality check prompt
- **Prompt Usage Guide**: `prompts/README.md` — how to use dual-mode prompt templates
- **Shared Scripts**: `scripts/README.md` — catalog and invocation conventions for `humanizer_check.py` (de-AI-tone gate), `_list_hits.py`, `_promote_draft.py` (draft→release sync), `_sync_draft.py` (errata write-back), `check_refs.py` (reference integrity, six buckets), `scan_hygiene.py` (CRLF / mojibake / junk / line budget), `init_subproject.py` (subproject scaffold), and the **review gate family**: `review_all.py` (all-in-one review report), `review_scale.py` (word-count), `review_continuity.py` (cross-chapter consistency), `review_rationality.py` (plot logic), `review_punctuation.py` (punctuation & orthography), backed by `_review_lib.py`. Scripts live in this repo only; invoke them from the subproject root. **Always write text with `newline='\n'`** — see `scripts/README.md`.
- **Subprojects**: `SUBPROJECTS.md` — registered independent novel subprojects (own git repo and remote), their locations and which scripts they consume.

## Constraints & Boundaries

1. **SKILL.md is index + quick-reference ONLY** — no code templates, no long-form methodology. All templates live in `references/`.
2. **No file exceeds 500 lines** — split into sub-modules when approaching the limit (see `references/method-patterns.md` split protocol). Ledgers, logs and generated seed files are exempt **but must be declared** via `scan_hygiene.py --allow`. See `references/subproject-playbook.md` Section 10.
3. **`prompts/` folder is DUAL-MODE** — files are standalone copy-paste templates for humans, NOT for agent auto-invocation.
4. **Harness Engineering compliance** — constraint-before-generation, structured memory, verification gates, modular decomposition, and feedback loops are mandatory.
5. **Every module is independently usable** — no circular dependencies between modules; each has a single responsibility.
6. **Output language** — All generated novel content respects `{{OUTPUT_LANGUAGE}}`; infrastructure files remain in English.
7. **Dual licensing** — Skill infrastructure: GPL-3.0; Generated novel content: CC BY-NC-SA 4.0. Every novel file must include the CC license header.
8. **State persistence** — State is persisted in structured Markdown files, not in conversation context.
9. **Progressive disclosure** — Layer 1: SKILL.md (index) → Layer 2: references/ (templates) → Layer 3: examples/ (worked examples).
10. **Human-in-the-loop** — Publishing workflow requires manual Git tag creation; prompts enable human oversight.
