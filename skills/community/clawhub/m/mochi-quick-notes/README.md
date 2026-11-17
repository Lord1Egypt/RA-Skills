# Quick Notes and Tasks

[Simplified Chinese guide](README.zh-CN.md)

Edit and search notes and tasks, filter tags and due dates, and export Markdown and CSV.

## What it does

Edit and search notes and tasks, filter tags and due dates, and export Markdown and CSV.

## Usage examples

After installation, send any example below to your AI. Include the files or URLs it refers to.

```text
Add a task: buy an ABC-200 filter this weekend, tagged home.
```

```text
Find notes tagged renovation from the last month and list them by date.
```

```text
Mark buying the filter complete and export the remaining tasks as Markdown and CSV.
```

## Exported files

notes.md / notes.csv

Files stay in the active agent workspace, with paths and SHA256 receipts. Existing records and earlier exports are retained.

## Requirements

OpenClaw, a connected model, Node.js 24.16+, and read/write access to the current agent workspace.

## Installation and first use

### MochiLab Skills assistant (recommended)

[Set up and connect the assistant](https://mochilab.bz/Skills/Connect.aspx?lang=en), then send:

```text
Install mochi-quick-notes
```

### ClawHub

[Open the Skill page](https://clawhub.ai/hznetnewpower/skills/mochi-quick-notes), or run from the active agent workspace:

```text
npx clawhub@latest install @hznetnewpower/mochi-quick-notes
```

### GitHub

[Open the source folder](https://github.com/hznetnewpower/mochilab-free-skills/tree/main/skills/mochi-quick-notes). Download the repository ZIP and copy `skills/mochi-quick-notes` into the active agent workspace's `skills/` directory.

Start a new conversation after installation.

## Detailed operation contract

Read [SKILL.md](SKILL.md) for the exact workflow, commands, permission boundaries and supporting references. Use the active agent workspace and verify actual outputs.
