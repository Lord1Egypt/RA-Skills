# PROJECT KNOWLEDGE BASE

**Generated:** 2026-02-16 18:22 Asia/Shanghai  
**Commit:** N/A (not a git repository)  
**Branch:** N/A

## OVERVIEW
Python-based OpenCode ACP collaboration toolkit with one core client and three wrapper entrypoints.
Repository is intentionally flat: scripts + operational docs, no package/module hierarchy.

## STRUCTURE
```text
opencode-acp/
├── opencode_acp_client.py    # canonical ACP orchestration client
├── opencode_wrapper.py       # passthrough wrapper mode
├── opencode_monitor.py       # polling/monitor wrapper mode
├── opencode_realtime.py      # realtime-output wrapper mode
├── SKILL.md                  # workflow contract and operating rules
└── TEST.md                   # manual smoke-test procedure
```

## WHERE TO LOOK
| Task | Location | Notes |
|------|----------|-------|
| Main ACP workflow | `opencode_acp_client.py` | `start -> initialize -> session/new -> session/prompt -> monitor` |
| CLI flags and defaults | `opencode_acp_client.py` | `--project`, `--task`, `--timeout=600`, `--verbose`, `--quiet` |
| Wrapper behavior | `opencode_wrapper.py` | Simple subprocess passthrough |
| Polling monitor mode | `opencode_monitor.py` | Threaded monitor + periodic progress output |
| Realtime output mode | `opencode_realtime.py` | Streams child output directly |
| Collaboration rules | `SKILL.md` | `Rules` section is canonical policy source |
| Manual verification | `TEST.md` | Document-driven E2E smoke test |

## CODE MAP
LSP symbol server unavailable in this environment (`ruff` missing), so code map is inferred from AST + direct reads:

| Symbol | Type | Location | Refs | Role |
|--------|------|----------|------|------|
| `OpenCodeACPClient` | class | `opencode_acp_client.py` | N/A | Core ACP protocol client |
| `main` | function | `opencode_acp_client.py` | N/A | Canonical CLI entrypoint |
| `run_opencode_with_monitoring` | function | `opencode_wrapper.py` | N/A | Wrapper execution mode |
| `OpenCodeMonitor` | class | `opencode_monitor.py` | N/A | Background monitoring mode |
| `run_opencode_with_realtime_output` | function | `opencode_realtime.py` | N/A | Realtime streaming mode |

## CONVENTIONS
- Flat root-only layout; no `src/`, `tests/`, or package metadata files.
- Operational workflow follows `Plan -> Execute -> Verify` from `SKILL.md`.
- First-time target projects should run `/init-deep` before ACP collaboration.
- Verification is manual/doc-driven (`TEST.md`), not framework-driven.

## ANTI-PATTERNS (THIS PROJECT)
- Do not kill sessions prematurely (`SKILL.md` Rules section).
- Do not wait silently during long runs; monitor via `process action:log`.

## UNIQUE STYLES
- Script-level entrypoints (`if __name__ == "__main__":`) for all runtime files.
- Wrapper scripts hardwire invocation path to the core client in `/root/openclaw/skills/opencode-acp/...`.
- Progress UX uses human-readable status lines + emoji in wrappers.

## COMMANDS
```bash
# Run from repository root
# Recommended canonical run
python opencode_acp_client.py --project /path/to/project --task "..."

# Verbose mode
python opencode_acp_client.py --project /path/to/project --task "..." --verbose

# Custom timeout
python opencode_acp_client.py --project /path/to/project --task "..." --timeout 1200

# Optional wrapper modes
python opencode_wrapper.py <project_dir> <task> [timeout]
python opencode_monitor.py <project_dir> <task> [timeout]
python opencode_realtime.py <project_dir> <task> [timeout]
```

## NOTES
- No native CI/build pipeline files detected (`.github/workflows`, `Makefile`, package/task runners absent).
- No existing nested directories currently justify subdirectory `AGENTS.md` files.
- Manual smoke test expectation is documented in `TEST.md` (create temp project, run client, verify code change).
- Runtime scripts auto-bootstrap a per-skill `.venv` on first execution (requires Python 3.9+).
