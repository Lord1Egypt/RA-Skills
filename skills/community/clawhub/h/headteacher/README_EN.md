<div align="center">

# Headteacher.Skill

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://python.org)
[![AgentSkills](https://img.shields.io/badge/AgentSkills-Standard-green)](https://agentskills.io)

A skill for teachers and headteachers who want to manage class data and generate working documents with AI.

[中文](README.md)

</div>

## What it is

`Headteacher.Skill` focuses on two core abilities:

1. Record, read, and continuously update class data.
2. Generate specific Office files on demand.

Typical data work includes:

- one-time import of student rosters and historical records
- daily updates for scores, behavior, parent communication, and class duties
- longitudinal reading for one student across time
- horizontal reading for part of a class or the whole class at one time slice

Typical file outputs include:

- seat plans
- duty schedules
- parent meeting slides
- other Word / Excel / PowerPoint files based on class data

The default v1 backend is **Feishu Base**.  
`Notion` and `Obsidian` are reserved for later development.

Feishu access is routed by runtime:

- In OpenClaw, prefer the official OpenClaw Lark/Feishu plugin `openclaw-lark`
- In Codex, Claude Code, or other local agents, keep using the existing `lark-cli` path

## v1 scope

### Available now

- Feishu Base as the default backend
- standard headteacher data model
- migration inspection for existing Feishu Bases
- local artifact registry

### Planned later

- Notion
- Obsidian

## Install

You do not need to remember shell commands.

Just send this prompt to your agent tool:

```bash
Please install this skill for me: https://github.com/YZDame/headteacher-skill
```

Then tell the agent:

```bash
Please enable Headteacher.Skill and guide me through initializing a Feishu Base workspace first.
```

If the skill is running inside OpenClaw, Feishu Base setup should prefer the official OpenClaw Feishu plugin path instead of requiring `lark-cli` by default.

## Office skills

If you want this skill to generate Office files, your local agent environment should also have Office-related skills for:

- `.docx`
- `.xlsx`
- `.pptx`

Reference:

- Anthropic skills repository: [https://github.com/anthropics/skills/tree/main/skills](https://github.com/anthropics/skills/tree/main/skills)

## Example requests

- “Help me initialize a class workspace for Senior 1 Class 3.”
- “Import this student roster and historical scores.”
- “Show me Zhang San’s scores and daily performance in time order.”
- “Show me which students need attention after this monthly exam.”
- “Generate a new seat plan based on scores, gender, and height.”
- “Generate parent meeting slides from recent scores and daily records.”
