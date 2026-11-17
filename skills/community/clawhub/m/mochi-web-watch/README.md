# Web Change Subscriptions

[Simplified Chinese guide](README.zh-CN.md)

Watch selected webpage regions, retain baselines, filter noise, record differences and connect scheduled checks with chat delivery.

## Features

Watch selected webpage regions, retain baselines, filter noise, record differences and connect scheduled checks with chat delivery.

## Usage examples

After installation, send any example below to your AI. Include the files or URLs it refers to.

```text
Watch the announcement URL I provide, limit extraction to main, and save and show the initial baseline.
```

```text
Check this watch for changes and show added and removed content with the source URL.
```

```text
Schedule this watch hourly and notify this chat only about registration-related changes; verify the scheduled task.
```

The first run creates a baseline; later checks retain added and removed content. Scheduling and notifications use the current agent and selected chat account.

## Requirements

OpenClaw, a connected model, active-workspace access; Node.js 24.16+. Scheduled checks require native scheduler and messaging tools.

## Installation and first use

### MochiLab Skills assistant (recommended)

[Set up and connect the assistant](https://mochilab.bz/Skills/Connect.aspx?lang=en), then send:

```text
Install mochi-web-watch
```

### ClawHub

[Open the Skill page](https://clawhub.ai/hznetnewpower/skills/mochi-web-watch), or run from the active agent workspace:

```text
npx clawhub@latest install @hznetnewpower/mochi-web-watch
```

### GitHub

[Open the source folder](https://github.com/hznetnewpower/mochilab-free-skills/tree/main/skills/mochi-web-watch). Download the repository ZIP and copy `skills/mochi-web-watch` into the active agent workspace's `skills/` directory.

Start a new conversation after installation.

## Detailed operation contract

Read [SKILL.md](SKILL.md) for the exact workflow, commands, permission boundaries and supporting references. Use the active agent workspace and verify actual outputs.
