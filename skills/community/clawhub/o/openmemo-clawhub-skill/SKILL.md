# OpenMemo - Persistent Memory for OpenClaw Agents

Stop agents from repeating tasks. Give your AI long-term memory.

## The Problem

OpenClaw provides a basic memory system, but in real-world usage agents still:

- **Repeat the same tasks** — the agent deploys successfully, but runs the entire workflow again next time because it never recorded the result
- **Store memory as large documents** — chat history and MEMORY.md files help retrieve text, but agents also need to remember tasks they completed, decisions they made, and workflows that succeeded

## What OpenMemo Adds

OpenMemo introduces a **structured memory layer** designed for agent workflows. Instead of storing raw conversation text, OpenMemo records **experience events**.

```
Backend deployed using Docker Compose
Scene: deployment
Type: task_execution
```

Agents recall **actions and results**, not just text.

## Comparison

| Feature | Typical Long-Term Memory | OpenMemo Memory |
|---|---|---|
| Memory type | Document memory | Experience memory |
| Storage | Notes and logs | Structured events |
| Retrieval | Vector search | Scene + task recall |
| Task deduplication | No | Yes |
| Workflow reuse | No | Yes |

## Core Capabilities

### Persistent Memory

OpenMemo records structured experience from agent workflows: tasks completed, decisions made, workflows validated. These memories persist across sessions and can be recalled when similar tasks appear. Over time the agent accumulates **long-term operational knowledge**.

### Task Deduplication

OpenMemo introduces **task fingerprinting**. Before executing a task, the agent checks memory. If the task already succeeded, the agent can reuse the result, skip execution, or continue from the previous step. This prevents duplicate execution, wasted tokens, and repeated workflows.

### Scene-Aware Memory

OpenMemo detects the working context: `coding`, `research`, `debugging`, `deployment`. Only the most relevant memories are retrieved for the current task. This keeps context focused and efficient.

### Memory Inspector

A built-in dashboard lets you see what the agent remembers, memory ranking and recall results, and system health. The memory system becomes **transparent** instead of a black box.

### Local-First Architecture

All memory operations happen locally. No external dependencies, no cloud required, full privacy, lower latency.

```
OpenClaw Agent
      |
      v
OpenMemo Skill
      |
      v
OpenMemo Adapter (local)
      |
      v
OpenMemo Memory Engine
```

## Example

**Without OpenMemo:**

```
> deploy backend
  → agent rebuilds everything again
```

**With OpenMemo:**

```
> deploy backend
  → agent detects previous deployment
  → reuses workflow
```

The agent stops behaving like a script and starts behaving like a **system**.

## Tools

### recall_memory

Retrieve relevant memory from OpenMemo. Use this to recall past experience, decisions, and knowledge before executing tasks.

**Parameters:**
- `query` (string, required): The search query for memory recall
- `scene` (string, optional): Scene context (e.g., coding, debug, research, deployment)

### write_memory

Store structured memory event in OpenMemo. Use this after completing important tasks to save experience for future use.

**Parameters:**
- `content` (string, required): The memory content to store
- `scene` (string, optional): Scene context
- `type` (string, optional): Memory type — fact, decision, observation, preference

### check_task_memory

Check if a task has already been executed. Use this FIRST before starting any task to avoid duplication.

**Parameters:**
- `task_description` (string, required): Description of the task to check

## Rules

When executing tasks, follow these memory operating rules:

1. BEFORE starting any task, call `check_task_memory` with the task description. If a successful previous execution exists, reuse the result or skip.

2. Use `recall_memory` to retrieve relevant past experience before making decisions.

3. After completing important tasks, call `write_memory` to store structured experience: decisions made, successful approaches, errors resolved, key observations.

4. Always include the scene context (coding, debug, research, deployment) for better recall accuracy.

## Setup

Install the OpenMemo adapter locally:

```
pip install openmemo openmemo-openclaw
openmemo serve
```

Restart your agent. The Skill will automatically detect the adapter and activate persistent memory.

## Best Use Cases

- Coding agents
- DevOps automation
- Research agents
- Multi-step AI workflows

## Links

- GitHub: https://github.com/openmemoai/openmemo
- Adapter: https://github.com/openmemoai/openmemo-openclaw-adapter
