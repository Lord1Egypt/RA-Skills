# Notion Export Desk

[Simplified Chinese guide](README.zh-CN.md)

Index an existing Notion Markdown/CSV export with page references, table counts and source hashes.

## What it does

Index an existing Notion Markdown/CSV export with page references, table counts and source hashes.

## Examples

After installation, send an example with its required files or parameters.

```text
Index this Notion export and assemble its Markdown pages.
```

```text
Summarize the database columns and row counts in this export.
```

```text
List skipped attachments and source hashes for review.
```

## Runtime and scope

Python 3.10+, standard library only. Uses selected inputs in the current agent workspace and saves new report files.

In Notion use the page menu → Export → Markdown & CSV, then provide the resulting ZIP. Follow current official help at https://www.notion.com/help/export-your-content . This is an offline export reader, not an API connector, permission migration or full-fidelity backup.

## Requirements

Python 3.10+; standard library

## Installation and first use

First [connect the MochiLab Skills assistant](https://mochilab.bz/Skills/Connect.aspx?lang=en), then send:

```text
Install mochi-notion-export-desk
```

A free account can connect the assistant and download this free Skill. Each BOT should use its own MochiLab account. Alternatively, get the ZIP and put its Skill folder in the target workspace’s skills/ directory. Start a new conversation after installation.

## Detailed operation contract

Read [SKILL.md](SKILL.md) for the exact workflow, commands, permission boundaries and supporting references. Use the active agent workspace and verify actual outputs.
