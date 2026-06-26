# Ollama Task Orchestrator — Skill Specification

## Overview
Manage Ollama task queue and code generation on a remote worker machine via SSH.
Provides queue health checks and task execution with exclusivity locking.

## Commands

### `ollama status [clean] [--force] [--kill-ollama]`
Check queue status and Ollama server health.
- No args: show status only
- `clean`: remove stale locks (prompts if Ollama is busy)
- `clean --force`: remove stale locks without prompting
- `clean --kill-ollama`: stop and restart Ollama server to cancel active generation

### `ollama run <task>`
Execute a task on the worker machine. Available tasks:

| Task | Usage | Description |
|---|---|---|
| `ping` | `ollama run ping` | Check runner is alive |
| `codegen` | `ollama run codegen <instruction>` | Generate code via Ollama |
| `write` | `ollama run write <file> <instruction>` | Generate and write code to file |
| `test` | `ollama run test [suite]` | Run project tests |
| `exec` | `ollama run exec <command>` | Run arbitrary shell command |
| `list-projects` | `ollama run list-projects` | List available projects |

## Configuration
| Variable | Default | Description |
|---|---|---|
| `OLLAMA_WORKER_HOST` | `worker-mac` | SSH host alias |
| `OLLAMA_RUNNER_PATH` | `~/worker/runner` | Runner scripts path on worker |
| `WORKER_ROOT` | `$HOME/worker` | Worker root directory |
| `PROJECTS_DIR` | `$WORKER_ROOT/projects` | Projects directory |
| `DEFAULT_PROJECT` | _(none)_ | Default project for context |
| `OLLAMA_MODEL` | `qwen2.5-coder:32b` | Ollama model |
| `OLLAMA_URL` | `http://localhost:11434/api/generate` | Ollama API endpoint |

## Files
```
skill.py                  OpenClaw skill entry point
runner/
  queue_status.sh         Queue and server health checker
  run_task.sh             Task executor with Ollama integration
README.md                 Setup and usage guide
SKILL.md                  This file
```
