# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Purpose

This is a **Claude Code skill** repository that defines the `openspec-workflow` skill. It contains no executable code, tests, or build system—only a skill definition file (`SKILL.md`) that gets loaded by the Claude Code harness.

## Architecture

The skill implements an OpenSpec-based iterative development workflow. It's triggered when users request creation/development tasks or mention OpenSpec-related keywords.

### Key Components

- **SKILL.md**: The complete skill definition containing workflow steps, artifact formats, and trigger conditions
- No source code, tests, or build artifacts

## Workflow Overview

The skill follows a 5-step process:

1. **Explore** (optional) - Investigation when requirements unclear
2. **Propose** - Interactive creation of change artifacts (proposal, design, tasks, delta specs)
3. **Apply** - Sequential implementation of tasks with progress reporting
4. **Verify** - Three-dimensional validation (completeness, correctness, consistency)
5. **Archive** - Merge specs to baseline and move change to archive

### Critical Behavioral Constraints

- **Interactive confirmation required**: Each stage requires user approval before proceeding
- **Never auto-confirm**: Always ask before creating files or proceeding to next stage
- **Exception**: User explicitly says "直接搞" or "不用确认" (skip confirmation)

### Artifact Structure

All artifacts live under `openspec/` in the working directory:

```
openspec/
├── specs/              # Baseline specs (system truth)
├── changes/            # Active changes
│   └── <change-name>/
│       ├── proposal.md
│       ├── design.md
│       ├── tasks.md
│       └── specs/      # Delta specs
└── changes/archive/    # Completed changes
```

## Working with This Skill

Since this is a skill definition repo, "development" means editing `SKILL.md`:

- Changes to workflow steps or artifact formats go directly in `SKILL.md`
- No build/test/lint commands exist—skill is loaded as markdown
- Test changes by invoking the skill in a Claude Code session

## Trigger Conditions

The skill activates when:
- User asks to create, develop, or implement something
- User says "按 OpenSpec 流程来", "走 spec 流程", or "按规范开发"
- Any creation/iteration task is requested
