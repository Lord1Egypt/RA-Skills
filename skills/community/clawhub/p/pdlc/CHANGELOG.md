# Changelog

All notable changes to **AIFLC — the AI-* PDLC Family** are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project uses pre-release (beta) versioning until the first stable release.

## [0.1.0-beta.1] — Unreleased

First public beta of the AI-* PDLC Family — 11 injectable workflow packages for AI-assisted software delivery.

### Added
- **11 packages**, each independently installable and self-contained:
  AI-ILC (idea life cycle), AI-PILC (project initiation), AI-PPM (portfolio management),
  AI-FLO (flow orchestration), AI-POLC (product ownership), AI-UXD (UX design),
  AI-ADLC (architecture design), AI-DWG (workspace generator), AI-GCE (governance & compliance),
  AI-TGE (test governance), AI-DFE (data fabric).
- Sequential chain: AI-PILC → AI-POLC → AI-UXD → AI-ADLC → AI-DWG → AI-GCE + AI-TGE, with the
  optional portfolio layer (AI-ILC ⇢ AI-PILC ⇢ AI-PPM) and AI-FLO as the edge router.
- Cross-package governance: shared Management Framework spine, Naming & Ownership convention,
  Dashboard Framework, Communication Fabric (gate contracts, family bindings).
- Per-package agents and trigger shortcuts; family-scoped data fabric (AI-DFE) with the
  `DAT__` / `DFA__` / `DHC__` triggers and a dashboard extension.
- Multi-platform install guides (Kiro, Amazon Q, Cursor, Claude Code, Cline, GitHub Copilot,
  Codex, VS Code) plus an interactive installer (PowerShell + Bash).
- Apache 2.0 license + NOTICE attribution; CONTRIBUTING, CLA, SECURITY, and rollback policy.

[0.1.0-beta.1]: https://github.com/mbmd/AIPDLC/releases/tag/v0.1.0-beta.1
