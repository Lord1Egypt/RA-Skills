# Expense Tracker and Budgets

[Simplified Chinese guide](README.zh-CN.md)

Import CSV transactions with deduplication, calculate exact totals and budgets, and export ledgers.

## What it does

Import CSV transactions with deduplication, calculate exact totals and budgets, and export ledgers.

## Usage examples

After installation, send any example below to your AI. Include the files or URLs it refers to.

```text
Record today's CNY 32 lunch and CNY 18 transport under food and transport.
```

```text
Import this bill CSV, check duplicates first, and summarize income and expenses by month and category.
```

```text
Set this month's food budget to CNY 1,500 and generate a budget report and ledger CSV.
```

## Exported files

ledger.csv / budget-report.md

Files stay in the active agent workspace, with paths and SHA256 receipts. Existing records and earlier exports are retained.

## Requirements

OpenClaw, a connected model, Node.js 24.16+, and read/write access to the current agent workspace.

## Installation and first use

### MochiLab Skills assistant (recommended)

[Set up and connect the assistant](https://mochilab.bz/Skills/Connect.aspx?lang=en), then send:

```text
Install mochi-expense-tracker
```

### ClawHub

[Open the Skill page](https://clawhub.ai/hznetnewpower/skills/mochi-expense-tracker), or run from the active agent workspace:

```text
npx clawhub@latest install @hznetnewpower/mochi-expense-tracker
```

### GitHub

[Open the source folder](https://github.com/hznetnewpower/mochilab-free-skills/tree/main/skills/mochi-expense-tracker). Download the repository ZIP and copy `skills/mochi-expense-tracker` into the active agent workspace's `skills/` directory.

Start a new conversation after installation.

## Detailed operation contract

Read [SKILL.md](SKILL.md) for the exact workflow, commands, permission boundaries and supporting references. Use the active agent workspace and verify actual outputs.
