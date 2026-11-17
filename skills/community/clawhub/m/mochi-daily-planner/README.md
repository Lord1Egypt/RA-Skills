# Daily Planner and Review

[Simplified Chinese guide](README.zh-CN.md)

Build priority-based time blocks with breaks and backlog, revise plans and export schedules.

## What it does

Build priority-based time blocks with breaks and backlog, revise plans and export schedules.

## Usage examples

After installation, send any example below to your AI. Include the files or URLs it refers to.

```text
Plan my 9 AM–noon: report writing 90 minutes, email 30 minutes, filing 30 minutes; include breaks and save the plan.
```

```text
Add a one-hour afternoon meeting, revise today's plan, and list tasks that no longer fit.
```

```text
Review today using my actual completion notes and export tomorrow's time blocks.
```

## Exported files

daily-plan.md / time-blocks.csv

Files stay in the active agent workspace, with paths and SHA256 receipts. Existing records and earlier exports are retained.

## Requirements

OpenClaw, a connected model, Node.js 24.16+, and read/write access to the current agent workspace.

## Installation and first use

### MochiLab Skills assistant (recommended)

[Set up and connect the assistant](https://mochilab.bz/Skills/Connect.aspx?lang=en), then send:

```text
Install mochi-daily-planner
```

### ClawHub

[Open the Skill page](https://clawhub.ai/hznetnewpower/skills/mochi-daily-planner), or run from the active agent workspace:

```text
npx clawhub@latest install @hznetnewpower/mochi-daily-planner
```

### GitHub

[Open the source folder](https://github.com/hznetnewpower/mochilab-free-skills/tree/main/skills/mochi-daily-planner). Download the repository ZIP and copy `skills/mochi-daily-planner` into the active agent workspace's `skills/` directory.

Start a new conversation after installation.

## Detailed operation contract

Read [SKILL.md](SKILL.md) for the exact workflow, commands, permission boundaries and supporting references. Use the active agent workspace and verify actual outputs.
