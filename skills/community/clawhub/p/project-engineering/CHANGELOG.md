# Changelog

All notable changes follow semantic versioning.

## 1.0.2 - 2026-08-25

- Added a real greenfield mode for architecture design, constraint tracking, executable engineering baselines, and the first vertical slice.
- Separated greenfield decisions from existing-repository discovery so empty targets no longer require Git or invented implementation evidence.
- Made Git and Python mode-specific aids instead of package-wide load gates, preserving transparent read-only fallbacks for existing repositories.
- Reworked the bilingual introduction around when to use the Skill, what it changes, and when the lightweight path is enough.
- Refined discovery metadata for `repository architecture` and `coding agent` searches without adding unsupported permission fields.
- Narrowed the default prompt to architecture, legacy codebase, and cross-file changes while following the user's current language.
- Added an explicit local-capability boundary for repository reads, vetted read-only scripts, workspace writes, and separately authorized external actions.
- Upgraded GitHub Actions to Node 24-compatible `actions/checkout@v7` and `actions/setup-python@v7`.

## 1.0.1 - 2026-08-25

- Improved GitHub and ClawHub discovery metadata for codebase analysis, repository analysis, software architecture, legacy code, and code review searches.
- Moved installation and a reproducible read-only verification example to the README first screen.
- Added bilingual onboarding, CI/license trust signals, and direct feedback links.
- Clarified the inventory script's safety guarantees without making claims about unrelated Agent runtime behavior.

## 1.0.0 - 2026-08-21

- Initial public release.
- Added evidence-driven repository discovery and architecture guidance.
- Added risk-calibrated implementation, database, protocol, validation, and delivery workflows.
- Added a read-only cross-stack project inventory script and regression tests.
- Added Codex UI metadata and OpenClaw/ClawHub metadata.
