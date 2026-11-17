# Obsidian Vault Link Map

[Simplified Chinese guide](README.zh-CN.md)

Map Markdown wikilinks, backlinks, orphan notes and broken or ambiguous targets without changing the vault.

## What it does

Map Markdown wikilinks, backlinks, orphan notes and broken or ambiguous targets without changing the vault.

## Examples

After installation, send an example with its required files or parameters.

```text
Find broken wikilinks in this Obsidian vault.
```

```text
List orphan notes and ambiguous note names.
```

```text
Map project backlinks and heading references.
```

## Runtime and scope

Python 3.10+, standard library only. Uses selected inputs in the current agent workspace and saves new report files.

Ask for a selected vault copied or mounted into the active workspace. Do not scan another user’s home directory. This helper does not synchronize Obsidian or modify notes.

## Requirements

Python 3.10+; standard library

## Installation and first use

First [connect the MochiLab Skills assistant](https://mochilab.bz/Skills/Connect.aspx?lang=en), then send:

```text
Install mochi-obsidian-map
```

A free account can connect the assistant and download this free Skill. Each BOT should use its own MochiLab account. Alternatively, get the ZIP and put its Skill folder in the target workspace’s skills/ directory. Start a new conversation after installation.

## Detailed operation contract

Read [SKILL.md](SKILL.md) for the exact workflow, commands, permission boundaries and supporting references. Use the active agent workspace and verify actual outputs.
