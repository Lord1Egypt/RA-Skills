# OpenClaw Maintenance and Migration Desk

[Simplified Chinese guide](README.zh-CN.md)

Inspect one selected OpenClaw instance and its agent bindings, create verified private snapshots, compare changes and rehearse restoration in a new directory.

## Features

Inspect one selected OpenClaw instance and its agent bindings, create verified private snapshots, compare changes and rehearse restoration in a new directory.

## Usage examples

After installation, send any example below to your AI. Include the files or URLs it refers to.

```text
Inspect this OpenClaw instance's agents, workspaces and chat-account bindings, and list configuration issues.
```

```text
Back up the OpenClaw configuration and workspaces I specify into a private archive with a checksum manifest.
```

```text
Verify this backup, rehearse restoration in a new directory, and report results and differences.
```

Inspects one selected instance and exports verified snapshots, differences and restore rehearsals into new folders. Live updates, restarts and activation use the installed OpenClaw tools as separate operations.

## Requirements

Python 3.10+; installed OpenClaw CLI for live status checks

## Installation and first use

### MochiLab Skills assistant (recommended)

[Set up and connect the assistant](https://mochilab.bz/Skills/Connect.aspx?lang=en), then send:

```text
Install mochi-claw-maintenance
```

### ClawHub

[Open the Skill page](https://clawhub.ai/hznetnewpower/skills/mochi-claw-maintenance), or run from the active agent workspace:

```text
npx clawhub@latest install @hznetnewpower/mochi-claw-maintenance
```

### GitHub

[Open the source folder](https://github.com/hznetnewpower/mochilab-free-skills/tree/main/skills/mochi-claw-maintenance). Download the repository ZIP and copy `skills/mochi-claw-maintenance` into the active agent workspace's `skills/` directory.

Start a new conversation after installation.

## Detailed operation contract

Read [SKILL.md](SKILL.md) for the exact workflow, commands, permission boundaries and supporting references. Use the active agent workspace and verify actual outputs.
