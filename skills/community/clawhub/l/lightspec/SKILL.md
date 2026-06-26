---
name: LightSpec
description: AI-native spec-driven development tool. Create, manage, and apply specifications with your agent.
author: Marco Leong
version: 0.6.0
tags: ["spec-driven", "spec", "development", "planning", "workflow", "openspecs", "spec-kit", "kiro"]
---

# LightSpec Skill

LightSpec is a CLI tool that brings spec‑driven development to any AI‑assisted workflow. It helps you create feature specifications, track changes, and implement code based on those specs. This skill teaches your OpenClaw agent how to install, verify, update, uninstall, and use LightSpec effectively.

For more details on LightSpec, visit the [Lightspec repository](https://github.com/augmenter-dev/lightspec)

## Installation

LightSpec requires [Node.js](https://nodejs.org) (v18 or later). The agent can install it globally via npm:

```
npm install -g lightspec
```

If Node.js is not present, the agent should first install Node.js (platform‑specific instructions can be provided if needed).

## Verification

To confirm LightSpec is installed correctly, run:

```
lightspec --version
```

The agent should expect a version number like `1.2.3`. If the command fails, installation should be retried or the user notified.

## Updating

To update LightSpec to the latest version:

```
npm update -g lightspec
```

After updating, verify again with `lightspec --version`.

## Uninstalling

To remove LightSpec completely:

```
npm uninstall -g lightspec
```

## Basic Usage

All LightSpec commands follow the pattern:

```
lightspec [command] [options]
```

### Initialize a Project

Run inside a project directory to set up LightSpec:

```
lightspec init
```

This creates a `lightspec/` folder and injects instructions into `AGENTS.md` (if present). The agent can then use the generated structure.

### Create a New Feature Spec

```
lightspec change "User authentication"
```

Or using the `spec` subcommand (depending on version). The agent should inspect the output to see where the spec file was created (usually `lightspec/changes/<change-name>/spec.md`).

### List Existing Changes or Specs

```
lightspec list          # list active changes
lightspec list --specs  # list all specs
```

### View Interactive Dashboard

```
lightspec view
```

The agent can run this to get a high‑level overview of all changes and specs.

### Validate a Spec or Change

```
lightspec validate [change-name]
```

Checks for completeness and consistency.

### Apply a Change (Implement)

After a spec is approved, the agent can apply it to the codebase:

```
lightspec apply [change-name]
```

This command generates code or updates files based on the spec (implementation details depend on the project’s configuration).

### Show Details of a Change or Spec

```
lightspec show [change-name]
```

## Workflow Example

1. **Initialize project** (if not already done)
```
lightspec init
```

2. **Create a change proposal**
```
lightspec change "Add profile search filters by role and team"
```

3. **Read the generated spec**
The agent can use `read_file` to inspect `lightspec/changes/add-profile-search-filters/spec.md`.

4. **Ask the user what’s missing**
The agent can summarise the spec and point out gaps (e.g., missing acceptance criteria).

5. **Validate the spec**
```
lightspec validate add-profile-search-filters
```

6. **Implement after approval**
```
lightspec apply add-profile-search-filters
```

## Tips for the Agent

- Always confirm with the user before running commands that change files (e.g., `apply`, `init` in an existing project).
- Use `lightspec --help` or `lightspec help [command]` if you need more details about a subcommand.
- LightSpec respects `.lightspec/config.json` for custom paths – the agent can read that to understand project‑specific settings.
- Refer to the official LightSpec documentation for the most updated information, guidence and how to guide the user.

## ClawHub Installation

To install this skill from ClawHub, the user can run:

```
openclaw install lightspec
```

Once installed, the agent will automatically load this skill and be able to assist with LightSpec tasks.