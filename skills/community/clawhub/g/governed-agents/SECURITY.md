# Security

## Subprocess Credential Isolation

All subprocess invocations (Codex CLI, OpenClaw CLI, git) use a **strict environment allowlist**.
Only the following variables are forwarded:

| Variable | Codex | OpenClaw | Purpose |
|----------|:-----:|:--------:|---------|
| `HOME` | ✓ | ✓ | Home directory |
| `PATH` | ✓ | ✓ | Binary lookup |
| `TMPDIR` | ✓ | ✓ | Temporary files |
| `LANG` | ✓ | ✓ | Locale |
| `LC_ALL` | ✓ | ✓ | Locale |
| `NO_COLOR` | ✓ | ✓ | Disable ANSI colors |
| `GOVERNED_WORK_DIR` | ✓ | ✓ | Task working directory |
| `GOVERNED_DB_PATH` | ✓ | ✓ | Reputation DB path |
| `GOVERNED_AUTH_TOKEN` | — | ✓ | HTTP API auth |

**No bypass mechanism exists.** API keys (e.g. `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`) are never forwarded
to subprocesses. External CLIs must source their own credentials via their own configuration.

## Prompt-Injection Detection Patterns

The prompt-injection detector (`prompt_validator.py`) uses a small set of detection-only regex patterns to flag attempts to override or bypass prior instructions. These patterns are **not** used for filtering or transformation; they are only used for detection and reporting.
The presence of these strings in `prompt_validator.py` and `SECURITY.md` is intentional — they define the detection ruleset.

## Network Access

The skill makes outbound HTTP HEAD requests only during grounding-gate verification (checking URL reachability of cited sources). No data is exfiltrated; only HTTP status codes are evaluated.

## Filesystem Writes

All persistent writes are confined to `~/.openclaw/workspace/.state/governed_agents/`:
- `reputation.db` — SQLite database for agent reputation scores
- Temporary task directories under `/tmp/governed-*` are cleaned up after execution.
