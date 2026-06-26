# ollama-task-orchestrator

An [OpenClaw](https://openclaw.ai) skill that lets your AI agents queue and execute tasks on a local Ollama instance running on a worker Mac (or any machine accessible via SSH).

Agents can check Ollama's queue health, run code generation tasks, write files, run tests, or execute arbitrary shell commands — all through a simple `ollama status` / `ollama run` interface.

---

## Features

- **Queue status** — check if Ollama is idle, busy, or has stale locks
- **Code generation** — generate code from natural language instructions via Ollama
- **File writing** — generate and write code directly to project files
- **Exclusivity locking** — prevents concurrent Ollama calls that degrade output quality
- **SSH-based** — works from any OpenClaw agent on a VPS or remote machine
- **Fully configurable** — no hardcoded paths or hostnames

---

## Requirements

- A Mac (or Linux machine) with [Ollama](https://ollama.ai) installed and running
- SSH access from your OpenClaw host to the worker machine
- Python 3 on the worker machine
- `curl` on the worker machine

---

## Installation

### 1. Set up the runner on your worker machine

Clone the repo and run the installer on each machine you want to use as a worker:

```bash
git clone https://github.com/RajeshHuria/ollama-task-orchestrator.git
cd ollama-task-orchestrator
./install.sh
```

This installs the runner scripts to `~/worker/runner/` by default. To use a custom path:

```bash
RUNNER_DIR=/custom/path ./install.sh
```

To update the runner scripts later:

```bash
git pull && ./install.sh
```

### 2. Configure SSH

Make sure your OpenClaw host can SSH into the worker without a password prompt. Add an entry to `~/.ssh/config` on your OpenClaw host:

```
Host <your-worker-host-alias>
  HostName <your-worker-ip-or-hostname>
  User <your-username>
  IdentityFile ~/.ssh/id_ed25519
```

### 3. Add the skill to OpenClaw

Copy the skill directory into your OpenClaw skills directory:

```bash
cp -r ollama-task-orchestrator/ ~/.openclaw/skills/
```

Then add it to your agent(s) in `openclaw.json`:

```json
{
  "id": "your-agent",
  "skills": ["ollama-task-orchestrator"]
}
```

### 4. Configure

Set these environment variables on your **OpenClaw host** to match your setup:

| Variable | Default | Description |
|---|---|---|
| `OLLAMA_WORKER_HOST` | `worker-mac` | SSH host alias defined in `~/.ssh/config` |
| `OLLAMA_RUNNER_PATH` | `~/worker/runner` | Path to the runner scripts on the worker machine |

Set these on your **worker machine** (e.g. in `~/.zshrc` or `~/.bashrc`):

| Variable | Default | Description |
|---|---|---|
| `WORKER_ROOT` | `$HOME/worker` | Root working directory |
| `PROJECTS_DIR` | `$WORKER_ROOT/projects` | Directory containing your projects |
| `DEFAULT_PROJECT` | _(none — **must set** for codegen/write/test)_ | Project folder name used for context and file writes |
| `OLLAMA_MODEL` | `qwen2.5-coder:32b` | Ollama model to use — change to any model you have pulled |
| `OLLAMA_URL` | `http://localhost:11434/api/generate` | Ollama API endpoint |
| `OLLAMA_TIMEOUT` | `300` | Max seconds to wait for Ollama response before giving up. Increase for large models or slow hardware — local models can take a while to load on first run. |

> **Important:** `DEFAULT_PROJECT` and `OLLAMA_MODEL` have no automatic defaults tied to any specific project or model. Set `DEFAULT_PROJECT` to your project folder name and `OLLAMA_MODEL` to a model you have pulled with `ollama pull <model>`.

---

## Usage

### Check queue status

```
ollama status
```

Returns Ollama server health, active model, lock state, and queue file counts.

```
ollama status clean           # clear stale locks (prompts if Ollama is busy)
ollama status clean --force   # clear without prompting
```

### Run a task

```
ollama run ping
ollama run codegen "write a Python function to validate email addresses"
ollama run write src/utils.py "write a retry decorator with exponential backoff"
ollama run nl "write a retry decorator in src/utils.py"
ollama run "run tests for auth"
ollama run "add a retry decorator to src/utils.py"
ollama run "update src/api.py with a FastAPI endpoint for user login"
ollama run "generate a Go struct for a user profile"
ollama run --dry-run "add a retry decorator to src/utils.py"
ollama run --dry-run test auth
ollama run test
ollama run exec "ls $PROJECTS_DIR"
ollama run list-projects
```

---

## How it works

```
OpenClaw Agent
     │
     │  skill.py (SSH)
     ▼
Worker Mac
     ├── runner/queue_status.sh   — checks Ollama API + lock directory
     └── runner/run_task.sh       — sends prompts to Ollama, writes output
```

The skill uses a **lock directory** (`$WORKER_ROOT/queue/ollama.lock.d`) to enforce that only one task runs at a time. If a task crashes without releasing the lock, `ollama status clean` removes it safely.

---

## Using with Claude Code or Codex

The `runner/` scripts are plain bash with no OpenClaw dependency. They can be called over SSH from any tool that can run shell commands — including Claude Code and Codex.

See **[README-claude-code.md](README-claude-code.md)** for setup instructions and example prompts for both tools.

---

## License

MIT — see [LICENSE](LICENSE)
