---
name: flowforge
description: "Run structured multi-step workflows via FlowForge engine. Use when user requests step-by-step execution, structured workflows, or when a task needs enforced ordering (e.g., 'follow the workflow', 'use flowforge', 'step by step process'). Helps AI agents execute multi-step tasks without skipping critical steps."
---

# FlowForge Workflow Runner

Execute multi-step workflows defined in YAML files using the FlowForge state machine engine.

## Prerequisites

FlowForge CLI must be installed. Check with:

```bash
flowforge --version
```

If the command fails or is not found, run the setup flow in [setup.md](setup.md) before proceeding. Setup will install the CLI, create the workflows directory, and configure your workspace.

## When to Use FlowForge

Use FlowForge when:
- User explicitly requests "workflow", "step by step", or "use flowforge"
- Task has multiple sequential steps that shouldn't be skipped
- User wants enforced execution order (e.g., always test before submit)
- Task involves state that needs to persist across sessions

Don't use for simple one-off tasks or quick questions.

## My Workflows

<!-- This table maps user intents to workflow names. -->
<!-- When you notice the same intent matching the same workflow 2-3 times, add it here. -->
<!-- This saves a `flowforge list` lookup every time and makes triggering instant. -->

| Intent | Workflow |
|--------|----------|
| *(add your mappings here as you use FlowForge)* | |

**Self-updating rule:** When you match an intent to a workflow via `flowforge list` and it works well, add that mapping to the table above. Then update the `description` field in the YAML frontmatter at the top of this file to include the new trigger phrase — this is how OpenClaw knows when to activate this skill.

## Core Workflow

### 1. Find the Right Workflow

First check the **My Workflows** table above. If the user's intent matches an entry, use it directly.

If no match, fall back to discovery:

```bash
flowforge list
```

If no workflow matches user's intent, help them create one (see [yaml-format.md](references/yaml-format.md)).

### 2. Start or Resume

```bash
# Check for active instances
flowforge active

# If active instance exists → resume
flowforge status

# If no active instance → start new
flowforge start <workflow-name>
```

### 3. Execute Current Node

After `flowforge status`, you'll see:
- Current node name
- Task (natural language instruction)
- Next node or branches

**Execute the task as described.** The task field tells you exactly what to do.

For complex implementation tasks: delegate to appropriate tools or sub-agents.
For simple tasks: execute directly.

### 4. Advance to Next Node

After completing the task:

```bash
# Linear flow (no branches)
flowforge next

# Branching flow (multiple paths)
flowforge next --branch 1   # first condition
flowforge next --branch 2   # second condition
```

### 5. Repeat Until Complete

Continue the cycle:
1. `flowforge status` — see current task
2. Execute the task
3. `flowforge next` — advance
4. Repeat until terminal node

### 6. View History

```bash
flowforge log
```

Shows all nodes visited with timestamps.

## Creating New Workflows

If user needs a workflow that doesn't exist:

1. Ask about their process steps
2. Draft a YAML file (see [yaml-format.md](references/yaml-format.md))
3. Save to `workflows/` directory or workspace
4. Register with `flowforge define workflow.yaml`

See [references/examples/](references/examples/) for templates.

## YAML Format Quick Reference

```yaml
name: workflow-name
description: What this workflow does
start: first-node

nodes:
  first-node:
    task: Description of what to do
    next: second-node

  second-node:
    task: Another task
    branches:
      - condition: success
        next: final-node
      - condition: failure
        next: first-node

  final-node:
    task: Wrap up and report
    terminal: true
```

### Node Fields

- `task`: Natural language instruction (required)
- `next`: Single next node for linear flow
- `branches`: Array of `{condition, next}` for branching
- `terminal`: Set to `true` for end nodes

## Rules

- **Never skip nodes.** Execute every node's task before advancing.
- **Always check status.** Don't assume position — run `flowforge status`.
- **One task at a time.** Complete current node before looking ahead.
- **Post-run.** When a workflow reaches a terminal node, record what was done and the outcome. If your workspace has a memory or log system, write results there.
- **State persists.** Workflows survive session restarts.
- **Use reset sparingly.** Only reset if workflow is stuck or user requests it.

## Advanced Usage

### Multiple Workflows

If user has multiple active workflows:
```bash
flowforge active  # list all
flowforge status  # shows current default
```

### Reset Current Workflow

```bash
flowforge reset
```

Creates new instance from start node. Old history is preserved.

### Workflow Discovery

FlowForge auto-loads YAML files from:
- `./workflows/` in current directory
- `~/.flowforge/workflows/` in home directory

Users can drop workflow files into these directories and they're automatically available — no need to run `flowforge define`.

## Examples

### Example 1: Code Contribution

User: "Help me contribute to this project"

1. Check if contribution workflow exists: `flowforge list`
2. Start: `flowforge start code-contribution`
3. Execute each node:
   - study → read project structure
   - implement → write code
   - test → run tests
   - submit → create PR
   - verify → address feedback

### Example 2: Learning Workflow

User: "I want to study React hooks step by step"

1. Check for study workflow: `flowforge list`
2. If exists: `flowforge start study`
3. If not: help create YAML with nodes like:
   - discover → find resources
   - deep-read → read documentation
   - practice → write examples
   - reflect → note key concepts

### Example 3: Resume Interrupted Work

User returns after session ended mid-workflow:

1. `flowforge active` → shows interrupted workflow
2. `flowforge status` → shows current node
3. Continue from there

## Troubleshooting

**"No active instance"**: Run `flowforge start <workflow>`

**"Workflow not found"**: Run `flowforge list` to see available workflows

**Wrong node/stuck**: Use `flowforge reset` to restart workflow

**Need to modify workflow**: Edit YAML file, run `flowforge define workflow.yaml` to update

## See Also

- [setup.md](setup.md) — Installation and configuration
- [references/yaml-format.md](references/yaml-format.md) — Complete YAML specification
- [references/examples/](references/examples/) — Template workflows
