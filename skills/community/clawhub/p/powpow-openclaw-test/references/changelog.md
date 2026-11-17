# Changelog — powpow-publisher

Version history (no need to read at runtime; for maintenance/troubleshooting only).

## 1.0.5 — 2026-09-25

Renamed from powpow-openclaw-test to powpow-publisher. No functional changes.

- ClawHub keeps the old slug as a redirect: old links and `@durenzidu/powpow-openclaw-test` references keep resolving to this skill.
- SKILL.md frontmatter `name` fixed: `powpow_openclaw` (underscore violation) → `powpow-publisher`; internal headings and the README install command updated to match.

## 1.0.4 — 2026-09-25 (retroactive entry)

Store listing metadata refresh, published via CLI parameters (package file changes limited to the frontmatter version bump).

- Display name set to "PowPow Publisher — turn photos into travelogues, pin them to the map, create chat-capable digital humans"; 5 English topics and categories (communication/lifestyle/creative) added.
- Entry added retroactively to the local changelog (was omitted at release time).

## 1.0.3 — 2026-09-23

Content replaced: the old v1.0.2 command-style simulator (register /
createDigitalHuman / send / status, in-memory) is replaced by the full
instruction-style skill carried by `powpow-simple-en` v1.0.0 (English edition
of `powpow-simple` v5.7.3). `scripts/` are byte-identical to those packages;
only display name, install command, and this changelog differ.

- SKILL.md, README.md and `references/` taken from `powpow-simple-en` v1.0.0.
- Display name kept as `powpow_openclaw`; routable slug stays
  `powpow-openclaw-test`.
- Version bumped 1.0.2 → 1.0.3 (next registry patch).

## 1.0.0 — 2026-09-20

First release of the English edition. Forked from `powpow-simple` v5.7.3 with
feature parity; `scripts/` are byte-identical (SHA256-verified). Documentation
and metadata only — zero script changes.

- **Display name set to a functional title**: "PowPow Simple EN - Publish
  posts & digital humans to the public map" (mirroring the Chinese package's
  descriptive display name; the routable slug stays `powpow-simple-en`).

- **SKILL.md fully translated to English**: triggers (English + Chinese
  phrases), conversation UX (tone table, opening templates, "next step" block),
  the full 8-step workflow, digital-human creation, error handling, and all
  hard rules.
- **Language policy added (hard rule)**: the conversation always follows the
  user's language — the English instructions serve users in any language.
- **Placeholders documented exactly as the script accepts them**: `{{dh}}` /
  `{{数字人}}`, `{{loc}}` / `{{位置}}`, `{{img}}` / `{{图}}` (the Chinese
  aliases are literal tokens recognized by compose.js — never invent new ones).
- **Honest localization notes added**: the platform's place search and
  digital-human library are currently strongest in Chinese; the preview page
  banner and the product UI shown in screenshots are Chinese-language.
- **README.md translated**, including Notes for reviewers (reviewer-facing
  context previously added in the Chinese package's 5.7.3).
- **references/ translated**: security.md, file-structure.md, screenshots.md.

## Inherited history (from powpow-simple-en / powpow-simple)

This package inherits all behavior of `powpow-simple-en` v1.0.0, itself the
English edition of `powpow-simple` (Chinese). Key milestones:

- **5.7.3 — 2026-09-19**: audit-noise reduction (description capability list,
  security.md rewrite, reviewer notes, session-path doc fixes). No script changes.
- **5.7.2 — 2026-09-19**: removed the incorrect "likes revive bubbles" claim;
  added product screenshots (6 images + jsdelivr mirror). No script changes.
- **5.7.1 — 2026-09-18**: `POWPOW_PASSWORD` env var renamed (fixing a
  long-standing "PowWow" typo).
- **5.7.0 — 2026-09-18**, **5.6.0 / 5.5.0 — 2026-09-18**, **5.4.1 / 5.4 — 2026-09-17**,
  **5.3 — 2026-09-17**: earlier evolution of the multi-script pipeline
  (login/session handling, compose placeholder hard-fail semantics, geocode
  degradation flow, digital-human creation, health filtering). Full details:
  the Chinese package's `references/changelog.md`.
