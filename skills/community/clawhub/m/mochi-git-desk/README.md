# Git Project Review and Snapshots

[Simplified Chinese guide](README.zh-CN.md)

Inspect a selected Git project and commit history, distinguish staged changes and create verified private working snapshots.

## Features

Inspect a selected Git project and commit history, distinguish staged changes and create verified private working snapshots.

Runs in the active agent workspace with local state. Supply your own account settings for mail, cloud storage or calendars. Scheduled notifications use OpenClaw scheduling.

## Usage examples

After installation, send any example below to your AI. Include the files or URLs it refers to.

```text
Inspect the Git project I specify and separately list staged, unstaged and untracked files.
```

```text
Read the last ten commits in this project and summarize the changes.
```

```text
Create a private working snapshot of this project, include the untracked files I select, and generate a checksum manifest.
```

## Requirements

Python 3.10+; standard library; Git CLI

## Installation and first use

### MochiLab Skills assistant (recommended)

[Set up and connect the assistant](https://mochilab.bz/Skills/Connect.aspx?lang=en), then send:

```text
Install mochi-git-desk
```

### ClawHub

[Open the Skill page](https://clawhub.ai/hznetnewpower/skills/mochi-git-desk), or run from the active agent workspace:

```text
npx clawhub@latest install @hznetnewpower/mochi-git-desk
```

### GitHub

[Open the source folder](https://github.com/hznetnewpower/mochilab-free-skills/tree/main/skills/mochi-git-desk). Download the repository ZIP and copy `skills/mochi-git-desk` into the active agent workspace's `skills/` directory.

Start a new conversation after installation.

## Detailed operation contract

Read [SKILL.md](SKILL.md) for the exact workflow, commands, permission boundaries and supporting references. Use the active agent workspace and verify actual outputs.
