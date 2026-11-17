# Reminders and Scheduled Tasks

[Simplified Chinese guide](README.zh-CN.md)

Audit scheduler jobs, record real delivery receipts and export calendar events.

## What it does

Audit scheduler jobs, record real delivery receipts and export calendar events.

## Usage examples

After installation, send any example below to your AI. Include the files or URLs it refers to.

```text
Remind me in this chat every Friday at 8 PM Asia/Shanghai to submit my weekly report; show the task ID and next run.
```

```text
Inspect my reminder tasks and list scheduled times and available delivery receipts.
```

```text
Export tomorrow's 3 PM medical follow-up reminder as an ICS file for my phone calendar.
```

## Exported files

reminder.ics / receipt.md

Files stay in the active agent workspace, with paths and SHA256 receipts. Existing records and earlier exports are retained.

## Requirements

OpenClaw, a connected model, Node.js 24.16+, and read/write access to the current agent workspace. OpenClaw scheduling tools, a running Gateway, and delivery support for the active chat channel. First use checks tool availability and the account route.

## Installation and first use

### MochiLab Skills assistant (recommended)

[Set up and connect the assistant](https://mochilab.bz/Skills/Connect.aspx?lang=en), then send:

```text
Install mochi-reminders
```

### ClawHub

[Open the Skill page](https://clawhub.ai/hznetnewpower/skills/mochi-reminders), or run from the active agent workspace:

```text
npx clawhub@latest install @hznetnewpower/mochi-reminders
```

### GitHub

[Open the source folder](https://github.com/hznetnewpower/mochilab-free-skills/tree/main/skills/mochi-reminders). Download the repository ZIP and copy `skills/mochi-reminders` into the active agent workspace's `skills/` directory.

Start a new conversation after installation.

## Detailed operation contract

Read [SKILL.md](SKILL.md) for the exact workflow, commands, permission boundaries and supporting references. Use the active agent workspace and verify actual outputs.
