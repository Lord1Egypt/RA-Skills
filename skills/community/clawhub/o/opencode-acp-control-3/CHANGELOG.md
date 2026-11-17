# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.3.0] - 2026-08-01

### Changed

- **SKILL.md rewritten** per issue #1 to be more concise, tool-agnostic, and
  operationally reliable. Standardized sections: Quick Reference, Protocol
  Rules, Standard Workflow (start, `initialize`, `session/new`, `session/prompt`,
  stream parsing, cancel), Resume Session, Polling/Timeout Strategy, Failure
  Modes, Update procedure, Implementation Notes.
- Frontmatter `description` now states trigger conditions and intended
  programmatic use; non-standard metadata fields removed.
- All examples use opaque session ids, newline-delimited JSON-RPC framing,
  and notification handling. Host-specific `process.write/poll/kill` API
  assumptions removed from `SKILL.md` in favor of tool-agnostic guidance.
- Examples normalize `cwd` to absolute paths and use deterministic JSON
  serialization.
- LICENSE copyright year bumped to 2026 (in repo, not displayed in this
  changelog).

### Added

- **`CODE_OF_CONDUCT.md`** — Contributor Covenant v2.1.
- **`CONTRIBUTING.md`** — How to file issues and PRs, local validation
  commands, style rules.
- **Issue templates** under `.github/ISSUE_TEMPLATE/` for bug reports and
  feature requests.
- **Pytest suite** in `tests/test_acp_demo.py` (12 tests) covering the
  `frame()` and `read_frame()` helpers plus CLI smoke tests for `--help`,
  `--dry-run`, and `--dry-run --no-prompt`.
- **`pytest.ini`** — test discovery and strict markers.
- **CI now runs pytest** in addition to markdownlint, lychee, and ruff.
- **README badges** for license, protocol, OpenCode version, Python, CI,
  version, and release.
- **`.gitignore`** extended to ignore test caches and virtualenvs.

### Fixed

- `acp_demo.py` `clientInfo.version` aligned to `0.3.0` (was `0.2.0`).
- `_meta.json` `version` aligned to `0.3.0` (was `0.2.0`).

## [0.2.0] - 2026-06-06

### Fixed

- `SKILL.md` `initialize` example identified itself as `clawdbot`/`Clawdbot` v1.0.0; corrected to `opencode-acp-control` / `OpenCode ACP Control` v0.2.0.
- `SKILL.md` release-check URL pointed at `anomalyco/opencode` (404). Corrected to `sst/opencode`.
- `SKILL.md` `updateOpenCode()` example also pointed at `anomalyco/opencode`; corrected to `sst/opencode`.
- `SKILL.md` install URL was `opencode.dev`. Corrected to `opencode.ai`.
- Added safety note alongside the `curl | bash` install command.
- `README.md` referenced a non-existent `hermes skill install` subcommand. Replaced with the two real copy-into-skills-dir patterns.
- Version drift: `_meta.json` said `0.1.0`, `SKILL.md` frontmatter said `1.0.2`. Aligned both to `0.2.0`.

### Added

- `examples/acp_demo.py` — runnable Python script that talks to a live `opencode acp` process over stdio JSON-RPC. Sends `initialize` + `session/new` and (optionally) a `session/prompt`, then streams `session/update` notifications until completion. Uses newline-delimited JSON framing (not LSP `Content-Length`) — matches OpenCode's actual transport. Includes `--dry-run` and `--no-prompt` modes for environments without an LLM provider configured.
- `.github/workflows/ci.yml` — CI that runs `markdownlint-cli` on every `.md`, fails if any of the URLs documented in `SKILL.md` / `README.md` / `CHANGELOG.md` return a non-2xx status (via `lychee`), and byte-compiles the demo script with Python 3.11.
- This `CHANGELOG.md`.

## [0.1.0] - 2026-01-29

### Added

- Initial public release: `SKILL.md` describing the OpenCode ACP workflow (initialize, session/new, session/prompt, session/cancel, session/load, update detection).
- `_meta.json` registry metadata.
- `README.md` with quick-start, tool mapping, and license.
- `LICENSE` (MIT).
