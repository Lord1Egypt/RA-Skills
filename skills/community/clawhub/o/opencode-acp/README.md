# opencode-acp

Python toolkit for collaborating with OpenCode through ACP (Agent Client Protocol).

It provides one canonical ACP client and three wrapper entrypoints for different runtime output styles.

## What This Project Does

- Starts `opencode acp`
- Initializes ACP JSON-RPC connection
- Creates a session and sends a task prompt
- Streams progress/tool updates
- Stops the ACP process on completion

Core workflow in `opencode_acp_client.py`:

`start -> initialize -> create_session -> send_task -> monitor_progress -> stop`

## Project Layout

```text
opencode-acp/
├── opencode_acp_client.py   # canonical ACP client
├── opencode_wrapper.py      # passthrough + realtime merged output
├── opencode_monitor.py      # polling/monitor style wrapper
├── opencode_realtime.py     # realtime output wrapper
├── runner_utils.py          # shared command builder for wrappers
├── venv_utils.py            # per-skill auto .venv bootstrap
├── SKILL.md                 # skill contract and workflow rules
├── TEST.md                  # manual smoke-test guide
├── CHANGELOG.md             # change history
└── test_opencode_smoke.py   # minimal automated smoke tests
```

## Requirements

- OpenCode binary available in PATH (`opencode`), or set `OPENCODE_BIN`
- Python 3.9+

### Model Configuration

This skill does not support selecting model per run.

Configure the default model in OpenCode config first, then use this skill:

- Config file: `~/.opencode/opencode.json`
- Example: set your desired default model in that file before running `opencode_acp_client.py`

### Auto Virtual Environment

On first run, entry scripts auto-create a local `.venv` in this skill directory and re-exec inside it.

- Scope: only this skill directory
- Minimum version: Python 3.9+
- Interpreter fallback: tries `python3.12/3.11/3.10/3.9`, then `python3`, `python` (Windows also `py -3.x`)
- Optional override: `OPENCODE_ACP_PYTHON=/path/to/python3.11`

## Quick Start

Run from repository root:

```bash
python opencode_acp_client.py --project /path/to/project --task "Add --version flag to CLI"
```

Verbose mode:

```bash
python opencode_acp_client.py --project /path/to/project --task "Refactor auth module" --verbose
```

Custom timeout:

```bash
python opencode_acp_client.py --project /path/to/project --task "Build REST API" --timeout 1200
```

Wrapper modes:

```bash
python opencode_wrapper.py <project_dir> <task> [timeout]
python opencode_monitor.py <project_dir> <task> [timeout]
python opencode_realtime.py <project_dir> <task> [timeout]
```

## Execution Modes

`opencode_acp_client.py` supports three modes:

- `oneshot` (default): one prompt, one completion, then exit
- `interactive`: terminal chat loop in a single ACP session (type `:exit` to quit)
- `session`: persisted pseudo-interactive mode for multi-call usage (useful for OpenClaw orchestration)

### Interactive Mode (single terminal session)

```bash
python opencode_acp_client.py --mode interactive --project /path/to/project
```

Optional first prompt:

```bash
python opencode_acp_client.py --mode interactive --project /path/to/project --task "Initial request"
```

### Session Mode (multi-call workflow)

Create a persisted session:

```bash
python opencode_acp_client.py --mode session --session-name demo --session-action start --project /path/to/project
```

Send follow-up prompts across separate calls:

```bash
python opencode_acp_client.py --mode session --session-name demo --session-action ask --task "Implement API layer"
python opencode_acp_client.py --mode session --session-name demo --session-action ask --task "Now add tests"
```

Inspect or remove session state:

```bash
python opencode_acp_client.py --mode session --session-name demo --session-action status
python opencode_acp_client.py --mode session --session-name demo --session-action stop
```

Persisted session files are stored under `.acp_sessions/` in this skill directory.

## Validation

Automated smoke tests:

```bash
python -m unittest -v test_opencode_smoke.py
```

Syntax check:

```bash
python -m py_compile opencode_acp_client.py opencode_wrapper.py opencode_monitor.py opencode_realtime.py runner_utils.py venv_utils.py test_opencode_smoke.py
```

Manual test flow is documented in `TEST.md`.

## Notes

- This repository is script-oriented (no Python packaging metadata yet).
- For first-time target projects in OpenCode workflow, see `/init-deep` guidance in `SKILL.md`.
- Current validation scope: tested only in OpenClaw environment.
