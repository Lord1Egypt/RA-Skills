# WebDAV Cloud File Desk

[Simplified Chinese guide](README.zh-CN.md)

Connect a WebDAV drive, list and compare a directory, upload or download files, check versions and produce integrity hashes.

## Features

Connect a WebDAV drive, list and compare a directory, upload or download files, check versions and produce integrity hashes.

Runs in the active agent workspace with local state. Supply your own account settings for mail, cloud storage or calendars. Scheduled notifications use OpenClaw scheduling.

## Usage examples

After installation, send any example below to your AI. Include the files or URLs it refers to.

```text
Using my configured WebDAV account, list files and sizes under /Documents.
```

```text
Compare local reports with the remote Reports directory and prepare an upload plan showing conflicts.
```

```text
Download the remote files I select into a new directory, check version changes, and generate SHA256 checksums.
```

## Requirements

Python 3.10+; standard library

## Installation and first use

### MochiLab Skills assistant (recommended)

[Set up and connect the assistant](https://mochilab.bz/Skills/Connect.aspx?lang=en), then send:

```text
Install mochi-cloud-files
```

### ClawHub

[Open the Skill page](https://clawhub.ai/hznetnewpower/skills/mochi-cloud-files), or run from the active agent workspace:

```text
npx clawhub@latest install @hznetnewpower/mochi-cloud-files
```

### GitHub

[Open the source folder](https://github.com/hznetnewpower/mochilab-free-skills/tree/main/skills/mochi-cloud-files). Download the repository ZIP and copy `skills/mochi-cloud-files` into the active agent workspace's `skills/` directory.

Start a new conversation after installation.

## Detailed operation contract

Read [SKILL.md](SKILL.md) for the exact workflow, commands, permission boundaries and supporting references. Use the active agent workspace and verify actual outputs.
