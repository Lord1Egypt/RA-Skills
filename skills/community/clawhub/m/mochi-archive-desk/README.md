# Archive and Integrity Toolbox

[Simplified Chinese guide](README.zh-CN.md)

Inspect ZIP/TAR contents, extract into new folders, create ZIPs from selected files and report per-file integrity hashes.

## Features

Inspect ZIP/TAR contents, extract into new folders, create ZIPs from selected files and report per-file integrity hashes.

Runs in the active agent workspace with local state. Supply your own account settings for mail, cloud storage or calendars. Scheduled notifications use OpenClaw scheduling.

## Usage examples

After installation, send any example below to your AI. Include the files or URLs it refers to.

```text
Inspect the uploaded backup.zip: list files, sizes and suspicious paths without extracting it.
```

```text
Extract backup.zip into a new directory and generate a file list with SHA256 checksums.
```

```text
Create documents.zip from the three files I specify and verify its integrity.
```

## Requirements

Python 3.10+; standard library

## Installation and first use

### MochiLab Skills assistant (recommended)

[Set up and connect the assistant](https://mochilab.bz/Skills/Connect.aspx?lang=en), then send:

```text
Install mochi-archive-desk
```

### ClawHub

[Open the Skill page](https://clawhub.ai/hznetnewpower/skills/mochi-archive-desk), or run from the active agent workspace:

```text
npx clawhub@latest install @hznetnewpower/mochi-archive-desk
```

### GitHub

[Open the source folder](https://github.com/hznetnewpower/mochilab-free-skills/tree/main/skills/mochi-archive-desk). Download the repository ZIP and copy `skills/mochi-archive-desk` into the active agent workspace's `skills/` directory.

Start a new conversation after installation.

## Detailed operation contract

Read [SKILL.md](SKILL.md) for the exact workflow, commands, permission boundaries and supporting references. Use the active agent workspace and verify actual outputs.
