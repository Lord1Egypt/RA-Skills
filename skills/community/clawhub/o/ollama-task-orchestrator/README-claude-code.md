# Using with Claude Code and Codex

The `runner/` scripts in this repo are plain bash — no OpenClaw required. You can call them directly from Claude Code or Codex via SSH.

---

## Claude Code

### Setup

Make sure Claude Code can SSH into your worker machine. Add an entry to `~/.ssh/config`:

```
Host <your-worker-host-alias>
  HostName <your-worker-ip-or-hostname>
  User <your-username>
  IdentityFile ~/.ssh/id_ed25519
```

### Tell Claude Code about the runner

Add a `CLAUDE.md` file to your project root so Claude Code knows the scripts exist:

```markdown
## Ollama Runner (worker machine)

For code generation tasks that should run locally on the worker machine, use:

- Check Ollama status:
  `ssh <your-worker-host-alias> '~/worker/runner/queue_status.sh'`

- Generate code:
  `ssh <your-worker-host-alias> 'DEFAULT_PROJECT=<project> OLLAMA_MODEL=<model> ~/worker/runner/run_task.sh codegen "<instruction>"'`

- Write code to file:
  `ssh <your-worker-host-alias> 'DEFAULT_PROJECT=<project> OLLAMA_MODEL=<model> ~/worker/runner/run_task.sh write <relative/path/file.ext> "<instruction>"'`

- Run tests:
  `ssh <your-worker-host-alias> 'DEFAULT_PROJECT=<project> ~/worker/runner/run_task.sh test'`

- Check runner is alive:
  `ssh <your-worker-host-alias> '~/worker/runner/run_task.sh ping'`
```

### Example usage in Claude Code

Once `CLAUDE.md` is in place, you can ask Claude Code naturally:

> "Use the Ollama runner to generate a Python function that validates email addresses"

Claude Code will SSH into the worker and run:
```bash
ssh worker-mac 'DEFAULT_PROJECT=my-project OLLAMA_MODEL=qwen2.5-coder:7b ~/worker/runner/run_task.sh codegen "write a Python function to validate email addresses"'
```

---

## Codex (OpenAI)

### Setup

Same SSH config as above. Codex (via the CLI or API with shell tool access) can run bash commands directly.

### Tell Codex about the runner

Add a system prompt or project instruction file:

```
You have access to a local Ollama instance on a worker machine via SSH.

To generate code using the local model:
  ssh <your-worker-host-alias> 'DEFAULT_PROJECT=<project> OLLAMA_MODEL=<model> ~/worker/runner/run_task.sh codegen "<instruction>"'

To check if Ollama is running and the queue is clear:
  ssh <your-worker-host-alias> '~/worker/runner/queue_status.sh'

Always check queue status before running a generation task. If Ollama is busy, wait or use 'queue_status.sh clean --force' to clear stale locks.
```

### Example usage in Codex

```
User: Generate a Go struct for a user profile with name, email, and created_at fields using the local Ollama runner.

Codex runs:
  ssh worker-mac 'DEFAULT_PROJECT=my-project OLLAMA_MODEL=qwen2.5-coder:7b ~/worker/runner/run_task.sh codegen "write a Go struct for a user profile with name, email, and created_at"'
```

---

## Environment variables reference

Set these on the worker machine before running the scripts:

| Variable | Default | Description |
|---|---|---|
| `DEFAULT_PROJECT` | _(none)_ | Project folder name for context |
| `OLLAMA_MODEL` | `qwen2.5-coder:32b` | Model to use — must be pulled with `ollama pull <model>` |
| `OLLAMA_URL` | `http://localhost:11434/api/generate` | Ollama API endpoint |
| `OLLAMA_TIMEOUT` | `300` | Max seconds to wait — increase for large models |
| `WORKER_ROOT` | `$HOME/worker` | Root working directory |
| `PROJECTS_DIR` | `$WORKER_ROOT/projects` | Directory containing projects |

---

## Notes

- The runner uses a **lock directory** (`$WORKER_ROOT/queue/ollama.lock.d`) to prevent concurrent Ollama calls. If a job crashes and leaves a stale lock, run `queue_status.sh clean` to clear it.
- Generation output is printed to stdout. For the `write` command, the output is written directly to the file and `WROTE: <path>` is printed instead.
- For OpenClaw users, see the main [README.md](README.md).
