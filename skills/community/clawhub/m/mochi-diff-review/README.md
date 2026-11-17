# File Diff and Delivery Review

[Simplified Chinese guide](README.zh-CN.md)

Compare text, JSON, keyed CSV and directories, create delivery manifests and verify file additions, changes and hashes.

## Features

Compare text, JSON, keyed CSV and directories, create delivery manifests and verify file additions, changes and hashes.

Runs in the active agent workspace and saves results and reports while preserving source files.

## Usage examples

After installation, send an example to your AI with the relevant files or URLs.

```text
Compare these configuration JSON versions by actual fields rather than key ordering.
```

```text
Compare two CSV files by order ID for added, missing and changed records.
```

```text
Create a delivery manifest and verify received files for missing or changed content.
```

## Requirements

Python 3.10+; standard library

## Installation and first use

### MochiLab Skills assistant (recommended)

[Set up and connect the assistant](https://mochilab.bz/Skills/Connect.aspx?lang=en), then send:

```text
Install mochi-diff-review
```

Alternatively, get the ZIP on this page and place its Skill folder in the active workspace's `skills/` directory. Start a new conversation after installation.

## Detailed operation contract

Read [SKILL.md](SKILL.md) for the exact workflow, commands, permission boundaries and supporting references. Use the active agent workspace and verify actual outputs.
