# Inventory and Reorder Desk

[Simplified Chinese guide](README.zh-CN.md)

Track SKUs and warehouse movements, calculate stock and moving-average cost, and export reorder reports by currency.

## Features

Track SKUs and warehouse movements, calculate stock and moving-average cost, and export reorder reports by currency.

Runs in the active agent workspace and saves results and reports while preserving source files.

## Usage examples

After installation, send an example to your AI with the relevant files or URLs.

```text
Create SKU records with minimum stock and target replenishment levels.
```

```text
Record today’s receipts and issues, reject insufficient stock and avoid duplicate movement IDs.
```

```text
Export warehouse stock and reorder lists with separate currency totals.
```

## Requirements

Python 3.10+; standard library

## Installation and first use

### MochiLab Skills assistant (recommended)

[Set up and connect the assistant](https://mochilab.bz/Skills/Connect.aspx?lang=en), then send:

```text
Install mochi-inventory-desk
```

Alternatively, get the ZIP on this page and place its Skill folder in the active workspace's `skills/` directory. Start a new conversation after installation.

## Detailed operation contract

Read [SKILL.md](SKILL.md) for the exact workflow, commands, permission boundaries and supporting references. Use the active agent workspace and verify actual outputs.
