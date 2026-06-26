# opentangl-openclaw-plugin

OpenClaw plugin for [OpenTangl](https://opentangl.com) — the autonomous multi-repo development engine.

Once installed, your OpenClaw agent can propose tasks, run autopilot cycles, execute workflows, audit cross-repo wiring, and manage the merge pipeline — all from chat.

---

## Install

```bash
openclaw plugins install opentangl-openclaw-plugin
```

OpenClaw checks ClawHub first and falls back to npm automatically.

---

## Configuration

Add to your OpenClaw config:

```json5
{
  plugins: {
    entries: {
      opentangl: {
        enabled: true,
        config: {
          // Required: path to your OpenTangl workspace root
          // (the directory containing projects.yaml and tasks/)
          workdir: "/path/to/your/opentangl-workspace",

          // Optional: override the CLI binary or entry point
          // Defaults: tries 'opentangl' in PATH, then 'npx tsx src/cli.ts'
          // bin: "/usr/local/bin/opentangl",

          // Optional: CLI timeout in milliseconds (default: 120000)
          // Autopilot runs may need higher values
          // timeout: 300000,
        },
      },
    },
  },
}
```

To enable the mutating tools (propose, autopilot, workflows, merge), add them to your tool allowlist:

```json5
{
  tools: {
    allow: [
      "opentangl_propose",
      "opentangl_autopilot",
      "opentangl_run_workflow",
      "opentangl_next",
      "opentangl_wire",
      "opentangl_merge",
      "opentangl_prune",
      "opentangl_resume",
    ],
  },
}
```

---

## Tools

### Always available (read-only)

| Tool | What it does |
|------|-------------|
| `opentangl_queue` | Show task queue status with dependency readiness |
| `opentangl_projects` | List registered projects and their resolved paths |
| `opentangl_list_executions` | List recent workflow executions and their status |

### Optional (require explicit enable)

| Tool | What it does |
|------|-------------|
| `opentangl_propose` | Analyze codebase and propose tasks (`preview` or `queue` mode) |
| `opentangl_autopilot` | Run propose + execute cycles (writes code, opens PRs) |
| `opentangl_run_workflow` | Run a workflow YAML (`run` = outputs only, `auto` = write + commit) |
| `opentangl_next` | Execute the next eligible task in the queue |
| `opentangl_wire` | Read-only cross-repo wiring audit |
| `opentangl_merge` | Run the merge pipeline (CI wait, diff review, merge/escalate) |
| `opentangl_prune` | Remove terminal tasks and commit cleaned queue |
| `opentangl_resume` | Resume a failed workflow execution by ID |

---

## Prerequisites

- OpenTangl installed and configured (`projects.yaml`, `.env` with API key)
- `node`, `git`, `gh` CLI available in PATH
- `OPENAI_API_KEY` or `ANTHROPIC_API_KEY` set in the environment where OpenClaw runs

---

## Example chat usage

```
You: What's in the task queue?
Agent: [calls opentangl_queue] → shows pending/running/completed tasks

You: Propose some new tasks for the api project
Agent: [calls opentangl_propose with mode=preview, projects=api] → shows proposed tasks

You: Looks good, queue them up
Agent: [calls opentangl_propose with mode=queue, projects=api] → appends to queue

You: Run one task
Agent: [calls opentangl_next] → executes next eligible task

You: Run the full merge pipeline
Agent: [calls opentangl_merge] → creates PRs, waits for CI, merges
```

---

## Publishing to ClawHub

```bash
cd plugin
npm install
npm run build
clawhub publish . --slug opentangl-openclaw-plugin --name "OpenTangl Plugin" --version 0.1.0 --tags latest
```

---

## License

MIT
