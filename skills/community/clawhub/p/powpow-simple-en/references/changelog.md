# Changelog — powpow-simple-en

Version history (no need to read at runtime; for maintenance/troubleshooting only).

## 1.0.1 — 2026-09-25

Store listing metadata refresh (metadata only — no functional changes).

- Display name, search topics, and categories (communication/lifestyle/creative) upgraded to the powpow-register series standard.

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

## Inherited history (from powpow-simple, Chinese edition)

This package inherits all behavior of `powpow-simple` up to v5.7.3. Key
milestones of the Chinese package:

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
