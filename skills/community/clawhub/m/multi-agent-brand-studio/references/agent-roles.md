# Agent Roles — Capabilities & Responsibilities

## Overview

The system includes 5 specialized agents organized in a star topology, plus an on-demand Reviewer:

| Agent | Role | Key Strength |
|-------|------|-------------|
| Leader | Orchestrator | Task decomposition, quality control, owner communication |
| Creator | Content + Visual | Multi-language copywriting, image generation, brand voice |
| Worker | Leader's Executor | File ops, CLI, config changes, workspace maintenance |
| Researcher | Research Analyst | Web research, competitive analysis, trend identification |
| Engineer | Full-Stack Engineer | Code, automation, API integration, CLI tools |

**On-demand:**

| Agent | Role | Key Strength |
|-------|------|-------------|
| Reviewer | Quality Reviewer | Independent quality assessment (spawned when needed) |

## Detailed Profiles

### Leader
- **Access**: Full workspace, Telegram binding, sessions_send to all agents
- **Restrictions**: No exec, no apply_patch, no browser
- **Unique abilities**: Only agent with owner access; owns shared/ writes; manages approval queue

### Creator
- **Access**: Own workspace, shared/ (read), web search, image generation tools, exec (image generation — requires `tools.exec.safeBinTrustedDirs` to include tool binary paths)
- **Restrictions**: No apply_patch, no browser, no publishing
- **Output**: Copy + visuals as one package, tagged [PENDING APPROVAL]
- **Workflow**: Brief-first — reads brand profile, researches, writes copy, generates visuals

### Worker
- **Access**: Own workspace, shared/ (read), exec, edit, write
- **Restrictions**: No apply_patch, no browser
- **Output**: Execution results with file paths
- **Scope**: Executes specific tasks from Leader — file ops, CLI, config changes, workspace maintenance

### Researcher
- **Access**: Own workspace, shared/ (read), web search/fetch
- **Restrictions**: No exec, no browser, no code execution
- **Output**: Structured briefs with confidence levels and sources

### Engineer
- **Access**: Own workspace + exec (requires `tools.exec.safeBinTrustedDirs` for non-system paths), shared/ (read)
- **Restrictions**: No browser
- **Output**: Working code with tests, tagged [PENDING REVIEW]

### Reviewer
- **Access**: Read-only everywhere, web fetch for fact-checking
- **Restrictions**: No write, no exec, no edit, no browser — fully sandboxed
- **Output**: Structured verdicts ([APPROVE] or [REVISE])

## Tools Denied Matrix

| Tool | Leader | Creator | Worker | Researcher | Engineer | Reviewer |
|------|--------|---------|--------|-----------|----------|----------|
| exec | X | - | - | X | - | X |
| edit | - | - | - | X | - | X |
| apply_patch | X | X | X | X | - | X |
| write | - | - | - | - | - | X |
| browser | X | X | X | X | X | X |

`X` = denied, `-` = allowed

## Team Configurations

### Full Team (5 agents + Reviewer) — Recommended
All agents active. Best for multi-brand operations with high content volume.

### Lean Team (3 agents)
Leader + Creator + Engineer. Suitable for single-brand or low-volume operations. Research handled by Creator's lightweight research; no independent review; no dedicated Worker.

### Custom
Select any combination. Leader is always required.
