# Incremental Backup Vault

[Simplified Chinese guide](README.zh-CN.md)

Create content-addressed incremental snapshots, compare versions, verify hashes and restore files into a new directory.

## Features

Create content-addressed incremental snapshots, compare versions, verify hashes and restore files into a new directory.

Runs in the active agent workspace and saves results and reports while preserving source files.

## Usage examples

After installation, send an example to your AI with the relevant files or URLs.

```text
Back up this document folder, excluding caches and dependencies, while preserving originals.
```

```text
Create another snapshot and list added and changed files.
```

```text
Verify last week’s snapshot and restore it into a new folder with per-file hash checks.
```

## Requirements

Python 3.10+; standard library

## Installation and first use

### MochiLab Skills assistant (recommended)

[Set up and connect the assistant](https://mochilab.bz/Skills/Connect.aspx?lang=en), then send:

```text
Install mochi-backup-vault
```

Alternatively, get the ZIP on this page and place its Skill folder in the active workspace's `skills/` directory. Start a new conversation after installation.

## Detailed operation contract

Read [SKILL.md](SKILL.md) for the exact workflow, commands, permission boundaries and supporting references. Use the active agent workspace and verify actual outputs.
