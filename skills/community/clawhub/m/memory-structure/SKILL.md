---
name: memory-structure
version: 1.0.2
description: Enable AI to learn from mistakes and never repeat them. Error tracking, layered memory, regular self-reflection, continuous improvement.
---
# Skill: memory-structure

## Name
memory-structure

## Function
Copy existing memory structure to new environments, enabling other Agents to use the same memory system.

## Use Cases
- Quickly set up self-improvement framework for new Agents
- Unify memory organization across multiple Agents
- Establish standardized self-reflection process

## Skill Contents

This skill includes:

| File | Description |
|------|-------------|
| `memory.md` | Main memory file: preferences, patterns, rules (HOT tier) |
| `corrections.md` | Error correction log: "what I got wrong" and correct answers |
| `index.md` | Memory index: tracks all memory file updates |
| `heartbeat-state.md` | Heartbeat state: records self-reflection check timestamps and results |
| `heartbeat-rules.md` | Heartbeat rules: defines triggers and execution logic for self-reflection |
| `setup.md` | Setup guide: installation and configuration instructions |

## Usage

### 1. Install Skill
Using ClawHub:
```bash
clawhub install memory-structure
```

### 2. Initialize Memory Structure

Create memory directory in target workspace:
```bash
mkdir -p ~/self-improving/{domains,projects,archive}
```

Then manually create the following files (copy template contents below):

### 3. Regular Self-Reflection
After completing important tasks, Agent should update heartbeat-state.md with reflection results.

## Core Concepts

- **HOT Tier**: Memory files are hot-tier, high-frequency access
- **Corrections Log**: Errors are the source of improvement, must be recorded
- **Heartbeat**: Regular self-reflection to check if memory structure needs updates

## Dependencies
- No external dependencies
- Requires file system write permission
- Heartbeat interval configured in OpenClaw config (default: 30 minutes)
