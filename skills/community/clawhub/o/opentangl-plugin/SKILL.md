# OpenTangl Plugin for OpenClaw

This is an **OpenClaw plugin** (not a plain skill). It registers native tools into the OpenClaw agent runtime so you can operate OpenTangl entirely from chat.

Once installed, your agent gains 11 tools covering the full OpenTangl lifecycle: reading the queue, proposing tasks, running autopilot, executing workflows, auditing cross-repo wiring, and managing the merge pipeline.

---

## Install

```bash
openclaw plugins install opentangl-plugin
```

Then restart your gateway:

```bash
openclaw gateway restart
```

---

## Configure

Add to your OpenClaw config file:

```json5
{
  plugins: {
    entries: {
      opentangl: {
        enabled: true,
        config: {
          // Required: path to your OpenTangl workspace
          // (the directory containing projects.yaml and tasks/)
          workdir: "/path/to/your/opentangl-workspace",

          // Optional: override the CLI path if not in PATH
          // bin: "/usr/local/bin/opentangl",

          // Optional: timeout in ms (default 120000; increase for autopilot)
          // timeout: 300000,
        },
      },
    },
  },
}
```

To enable the mutating tools (they are off by default for safety):

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

## Prerequisites

- OpenTangl installed and configured (`projects.yaml` + `.env` with API key)
- `node`, `git`, `gh` in PATH
- `OPENAI_API_KEY` or `ANTHROPIC_API_KEY` in the environment

---

## What you get

### Always-on tools (read-only)

| Tool | What it does |
|------|-------------|
| `opentangl_queue` | Task queue with dependency status |
| `opentangl_projects` | Registered projects and resolved paths |
| `opentangl_list_executions` | Recent workflow executions |

### Optional tools (enable via `tools.allow`)

| Tool | What it does |
|------|-------------|
| `opentangl_propose` | Analyze codebase → propose tasks (`preview` or `queue`) |
| `opentangl_autopilot` | Full autopilot: propose + write + verify + commit + PR |
| `opentangl_run_workflow` | Run a workflow YAML (`run` or `auto` mode) |
| `opentangl_next` | Execute the next eligible queue task |
| `opentangl_wire` | Read-only cross-repo wiring audit |
| `opentangl_merge` | Merge pipeline: CI wait, diff review, merge/escalate |
| `opentangl_prune` | Remove terminal tasks, commit cleaned queue |
| `opentangl_resume` | Resume a failed workflow execution by ID |

---

## Example session

```
You:   What's in the task queue?
Agent: [opentangl_queue] → 3 pending, 1 running, 2 completed

You:   Propose some tasks for the api project
Agent: [opentangl_propose mode=preview projects=api] → shows proposed tasks

You:   Queue them
Agent: [opentangl_propose mode=queue projects=api] → appended 4 tasks

You:   Run the next one
Agent: [opentangl_next] → executes task, commits changes

You:   Run the merge pipeline
Agent: [opentangl_merge] → opens PRs, waits for CI, merges
```

---

## Related

- **OpenTangl skill** (`opentangl`) — onboarding guide for setting up OpenTangl from scratch
- **OpenTangl docs** — https://opentangl.com
