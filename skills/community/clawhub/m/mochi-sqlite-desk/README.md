# SQLite Query and Export Desk

[Simplified Chinese guide](README.zh-CN.md)

Inspect SQLite schemas, run bounded read-only queries, export CSV/JSON and import CSV into a fresh database.

## Features

Inspect SQLite schemas, run bounded read-only queries, export CSV/JSON and import CSV into a fresh database.

Runs in the active agent workspace and saves results and reports while preserving source files.

## Usage examples

After installation, send an example to your AI with the relevant files or URLs.

```text
Inspect the tables and columns in this SQLite file without changing it.
```

```text
Group order counts and amounts by month and export CSV while preserving the database.
```

```text
Import this CSV into a new SQLite file, preserve leading-zero IDs and verify integrity.
```

## Requirements

Python 3.10+; standard library

## Installation and first use

### MochiLab Skills assistant (recommended)

[Set up and connect the assistant](https://mochilab.bz/Skills/Connect.aspx?lang=en), then send:

```text
Install mochi-sqlite-desk
```

Alternatively, get the ZIP on this page and place its Skill folder in the active workspace's `skills/` directory. Start a new conversation after installation.

## Detailed operation contract

Read [SKILL.md](SKILL.md) for the exact workflow, commands, permission boundaries and supporting references. Use the active agent workspace and verify actual outputs.
