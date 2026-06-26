# Project Coordinator Skill

![Version](https://img.shields.io/badge/version-1.0.8-blue)
![License](https://img.shields.io/badge/license-MIT-green)

A skill for structuring multi-agent project execution with isolated session architecture.

## Installation

```bash
# Via ClawhHub
clawdhub install project-coordinator

# Via Git
git clone https://github.com/KaigeGao1110/Project-Coordinator ~/.openclaw/workspace/skills/project-coordinator
```

## Quick Start

Type `//start ` followed by your project description:

```
//start build a Chrome extension for Gmail
```

The skill spawns an isolated Project Coordinator session that:
1. Breaks work into independent tasks
2. Spawns subagents for parallel execution
3. Monitors progress and compiles results

## Architecture

```
Main Session (coordinator only - no direct tool calls)
  └── Project Coordinator (spawned per project, isolated run)
        └── Subagents (spawned by Coordinator, run tasks in parallel)
```

## Key Benefits

- **Token isolation**: Each project runs in its own session — old projects don't accumulate tokens in the main session
- **Clean separation**: Main session only coordinates; Coordinators handle execution
- **Parallel execution**: Subagents run tasks concurrently under the Coordinator
- **Safe archiving**: Uses archive-project skill — credential sanitization and human approval before any file deletion

## What the Coordinator Can Do

The Coordinator can run shell commands, read/write workspace files, and spawn subagents. These are standard project execution capabilities. All archiving follows the archive-project skill, which sanitizes credentials and requires human approval before deleting files.

## For AI Agents

Install into workspace skills directory. The SKILL.md contains the full workflow, architecture rules, and Coordinator pattern.

## Language

All output is in English.
