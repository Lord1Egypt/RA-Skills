---
name: openclaw-kilo-agent
description: "High-performance coding agent and browser automation orchestrator using the Kilo CLI. Use when you need to: (1) Offload heavy-duty coding tasks (refactoring, multi-file edits, complex implementations), (2) Execute browser automation workflows (scraping, form-filling, navigating websites), (3) Manage sessions and context across different Kilo runs, (4) Use MCP servers for extended capabilities (Puppeteer, GitHub, FileSystem). This skill is the 'hands' for OpenClaw's 'brain'."
---

# OpenClaw-Kilo-Agent

This skill coordinates the Kilo CLI to perform complex execution tasks, from deep codebase refactoring to automated browser interactions.

## Core Capabilities

- **Heavy-Lifting Coding**: Offload file-intensive tasks to the specialized Kilo agent.
- **Browser Automation**: Control web browsers via Puppeteer MCP integration.
- **Session Continuity**: Resume or fork existing Kilo sessions to maintain context.
- **Autonomous Execution**: Run Kilo with `--auto` for hands-free automation in OpenClaw.

## Setting Up Kilo

If Kilo is not yet configured, follow the instructions in [setup-guide.md](references/setup-guide.md).

**Key Config Location:** `~/.config/kilo/kilo.json`

## Workflow Pattern

For a detailed breakdown of the "Brain and Hands" execution strategy, see [workflow.md](references/workflow.md).

### 1. Basic Task Execution
To run a one-shot task with Kilo:
```bash
kilo run --model <model> --auto "<prompt>"
```

### 2. Browser Automation Task
To run a browser-based task using the Puppeteer MCP:
```bash
kilo run --model <model> --auto "Use your puppeteer MCP tool to navigate to <URL>, <actions>, and report back <results>."
```

### 3. Session Management
To list, continue, or fork sessions:
```bash
# List all sessions
kilo session list

# Continue the last session
kilo run --continue --model <model> --auto "<next task>"

# Fork a specific session
kilo run --session <sessionID> --fork --model <model> --auto "<experimental task>"
```

### 4. Monitoring Progress
If a task takes a long time, use the `process` tool to poll the Kilo run.

## Best Practices

- **Specify the Model**: Always use `--model <provider/model>` to ensure consistency (e.g., `kilo/minimax/minimax-m2.5:free`).
- **Use Auto-Approval**: Always include the `--auto` flag when running Kilo from OpenClaw to avoid hanging on permission prompts.
- **Prompt Engineering**: Be specific about the desired output. Kilo is powerful but benefits from clear, structured instructions.
- **Check Stats**: Use `kilo stats` to monitor token usage and costs.
