# Changelog
## 2.2.1 — 2026-11-17

发布面修正，无功能变更。

- **首屏重写**：首屏中文化（本地早已改好从未发）+ 补 4 个语义 tag
- **显示名**：发布时必须带 `--name "博物馆看展 · Museum Explorer"`（此前未能稳定带中文名）
- **检索面**：tags 刷新到 2.2.1 并补齐语义 tag（`museum,exhibition,travel,guide,notes`）；topics 同步为 `博物馆,看展,展览,观展,看展攻略`

## 2.2.1 — 2026-10-27

Front-screen copy only. No behavior, file, or dependency change.

- `description` reordered: the Chinese block now comes first, so the search-result line reads in Chinese before English. Motivation: on ClawHub the line under the title is this field; a Chinese-first reader sees an English paragraph and leaves before opening the skill.
- Every existing trigger was preserved verbatim, including the `Use when …` list and the nine named venues. The bundled bilingual rewrite from the 2026-10-27 batch dropped those triggers; this keeps them.

## 2.1.1 — 2026-09-29

Release-metadata fix only. No file content or behavior change.

- Restored the ClawHub display name to `Museum Visit Planner & Guide`. Publishing 2.1.0 without `--name` caused ClawHub to fall back to the raw slug.
- Release note: **always publish with `--name "Museum Visit Planner & Guide"`** — `clawhub publish --name "Museum Visit Planner & Guide" --slug museum-explorer --version <v>`.

## 2.1.0 — 2026-09-29

- Added a seventh venue starter pack: Jingdezhen China Ceramics Museum / 景德镇中国陶瓷博物馆 — a specialist ceramics museum, added as a different route pattern from the six general encyclopaedic collections (single-object-driven visit, vertical floors 4–7, guarded queued viewing at the viral piece, and a disambiguation note against similarly named Jingdezhen ceramic museums).
- Added `references/shareable-visit-content.md`: advisory-only guidance on post-visit sharing, covering the separate rights in an object, a photograph of it, the venue's photography rules, and a museum's own IP, plus a risk ladder from personal use to commercial listing.
- SKILL.md: new optional "Shareable Content" section with an explicit handoff boundary — this skill explains and advises, a dedicated image skill produces the artwork, and this skill never publishes.
- Description and "When to Use" extended to cover post-visit sharing questions; explicitly states the skill does not generate images or publish.
- No change to the three modes (Plan / Guide / Remember) or to existing venue packs.

## 2.0.1 — 2026-09-16

- Added an explicit instruction to follow the language of the user's current request.
- Clarified that bilingual labels and examples are optional illustrations.
- Replaced Chinese-only template placeholders with language-neutral placeholders.

## 2.0.0 — 2026-09-16

- Repositioned the skill as `Museum Visit Planner & Guide`.
- Replaced the mandatory three-stage workflow with three independent modes: Plan, Guide, and Remember.
- Added explicit 90-minute and 180-minute route contracts.
- Added a reusable Museum Visit Brief and Visit Memory template.
- Added stable starter orientation for six frequently requested Chinese museums.
- Added one completed historical example with an explicit expiry boundary.
- Simplified default behavior to conversation-first and no file writes unless requested.
- Preserved official-source verification, access dates, uncertainty labels, accessibility adaptation, and sensitive-history handling.
- Removed bundled live exhibition indexes, generated journals, preview images, and executable scripts from the published package.
