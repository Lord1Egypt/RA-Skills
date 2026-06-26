# Changelog

## 1.0.0

Initial public release.

### Added
- Junie-native install, update, auth, and config guidance
- Repo bootstrap support for `.junie/AGENTS.md`, `.junie/skills/`, `.junie/commands/`, `.junie/agents/`, `.junie/models/`, `.junie/mcp/`, and `.junie/rules/`
- Host-agent to Junie handoff guidance for iterative execution and review work
- Model posture reporting guidance for current/default model, provider, and effort
- Usage reporting guidance plus `scripts/summarize_junie_usage.py`
- Limited host-agent trigger phrases such as `/junie status`, `/junie model`, `/junie usage`, `/junie bootstrap`, and `/junie dry-run`

### Changed
- Prefer non-interactive/config-driven Junie setup before TUI driving
- Prefer package-manager installs when they fit; treat remote installer scripts as higher-trust operations
- Treat Junie CLI/TUI to IDE integration as aspirational unless the environment proves otherwise
- Use plain PTY/process control for normal Junie execution; escalate to `headless-terminal` only when rendered TUI state matters

### Hardening
- Added clearer trust boundaries around install/auth flows and durable secret storage
- Removed private/local project assumptions and optional local-context dependencies
- Generalized orchestration wording to `host agent` for better portability
