# Excel Business Analysis Studio

[Simplified Chinese guide](README.zh-CN.md)

Combine XLSX/CSV sources, clean mapped fields, deduplicate, reconcile sales, refunds and expenses, and export currency-separated monthly reports with source rows.

## Features

Combine XLSX/CSV sources, clean mapped fields, deduplicate, reconcile sales, refunds and expenses, and export currency-separated monthly reports with source rows.

## Usage examples

After installation, send any example below to your AI. Include the files or URLs it refers to.

```text
Merge my three monthly sales tables after checking column names and currencies; list duplicate and anomalous rows.
```

```text
Match sales with refunds, compare net amounts for this month and last month by currency, and export Excel.
```

```text
Clean these CSV files using my field mappings and produce summaries retaining source filenames and row numbers.
```

Outputs Excel reports, issue rows, source locations and reusable mappings. Keeps original files and separates currencies. Formula inspection lists formula cells; calculation uses your spreadsheet application.

## Requirements

Python 3.10+, openpyxl 3.1+

## Installation and first use

### MochiLab Skills assistant (recommended)

[Set up and connect the assistant](https://mochilab.bz/Skills/Connect.aspx?lang=en), then send:

```text
Install mochi-sheet-studio
```

### ClawHub

[Open the Skill page](https://clawhub.ai/hznetnewpower/skills/mochi-sheet-studio), or run from the active agent workspace:

```text
npx clawhub@latest install @hznetnewpower/mochi-sheet-studio
```

### GitHub

[Open the source folder](https://github.com/hznetnewpower/mochilab-free-skills/tree/main/skills/mochi-sheet-studio). Download the repository ZIP and copy `skills/mochi-sheet-studio` into the active agent workspace's `skills/` directory.

Start a new conversation after installation.

## Detailed operation contract

Read [SKILL.md](SKILL.md) for the exact workflow, commands, permission boundaries and supporting references. Use the active agent workspace and verify actual outputs.
