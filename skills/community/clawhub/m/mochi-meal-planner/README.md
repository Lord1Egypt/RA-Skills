# Meal Planner and Grocery List

[Simplified Chinese guide](README.zh-CN.md)

Save dietary exclusions and pantry stock, scale servings and export menus and groceries.

## What it does

Save dietary exclusions and pantry stock, scale servings and export menus and groceries.

## Usage examples

After installation, send any example below to your AI. Include the files or URLs it refers to.

```text
Save my preferences: two people, no peanuts; plan three dinners using the inventory I provide.
```

```text
Scale this recipe from two servings to four and list ingredient quantities.
```

```text
Combine this week's recipes into a grocery list, subtract existing inventory, and export CSV.
```

## Exported files

meal-plan.md / groceries.csv

Files stay in the active agent workspace, with paths and SHA256 receipts. Existing records and earlier exports are retained.

## Requirements

OpenClaw, a connected model, Node.js 24.16+, and read/write access to the current agent workspace.

## Installation and first use

### MochiLab Skills assistant (recommended)

[Set up and connect the assistant](https://mochilab.bz/Skills/Connect.aspx?lang=en), then send:

```text
Install mochi-meal-planner
```

### ClawHub

[Open the Skill page](https://clawhub.ai/hznetnewpower/skills/mochi-meal-planner), or run from the active agent workspace:

```text
npx clawhub@latest install @hznetnewpower/mochi-meal-planner
```

### GitHub

[Open the source folder](https://github.com/hznetnewpower/mochilab-free-skills/tree/main/skills/mochi-meal-planner). Download the repository ZIP and copy `skills/mochi-meal-planner` into the active agent workspace's `skills/` directory.

Start a new conversation after installation.

## Detailed operation contract

Read [SKILL.md](SKILL.md) for the exact workflow, commands, permission boundaries and supporting references. Use the active agent workspace and verify actual outputs.
