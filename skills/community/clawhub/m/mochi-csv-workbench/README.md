# CSV Cleaning and Analysis

[Simplified Chinese guide](README.zh-CN.md)

Clean CSV/TSV, review missing and duplicate values, and total exact amounts by an explicit grouping column.

## Features

Read UTF-8 CSV/TSV with BOMs, quoted delimiters and multiline cells. Export column statistics, missing-value and duplicate reports, plus formula-protected CSV. Decimal totals use exact arithmetic.

Exact duplicate rows are removed by default; use `--keep-duplicates` for repeated transactions. Select the grouping and amount columns to total each currency separately, with missing and invalid amounts listed.

## Usage examples

After installation, send any example below to your AI. Include the files or URLs it refers to.

```text
Check orders.csv for missing values and exact duplicate rows, and produce a data-quality report.
```

```text
Clean this CSV by removing exact duplicate rows, retaining the original and saving a new result.
```

```text
Group the amount column by customer and currency, use exact decimal arithmetic, and export a summary CSV.
```

## Advanced usage: run in a terminal

These commands are for manual execution in the terminal on the computer or server running OpenClaw. For everyday use, send one of the chat examples above.

Replace these placeholders with actual paths before running:

- `SKILL_DIRECTORY`: the installed Skill folder.
- `INPUT.csv`: the input CSV file.
- `NEW_OUTPUT_DIRECTORY`: a new output directory.

```text
node "SKILL_DIRECTORY/scripts/csv.mjs" --input "INPUT.csv" --out "NEW_OUTPUT_DIRECTORY" --group-by "currency" --sum-column "amount" --keep-duplicates
```

Replace paths and column names with the actual values. Try `samples/currency-input.en.csv` for the bundled English example.

## Requirements

OpenClaw with a connected model, Node.js 24.16+ or 26.1+, local command access and workspace read/write permission.

## Installation and first use

### MochiLab Skills assistant (recommended)

[Set up and connect the assistant](https://mochilab.bz/Skills/Connect.aspx?lang=en), then send:

```text
Install mochi-csv-workbench
```

### ClawHub

[Open the Skill page](https://clawhub.ai/hznetnewpower/skills/mochi-csv-workbench), or run from the active agent workspace:

```text
npx clawhub@latest install @hznetnewpower/mochi-csv-workbench
```

### GitHub

[Open the source folder](https://github.com/hznetnewpower/mochilab-free-skills/tree/main/skills/mochi-csv-workbench). Download the repository ZIP and copy `skills/mochi-csv-workbench` into the active agent workspace's `skills/` directory.

Start a new conversation after installation.

## Detailed operation contract

Read [SKILL.md](SKILL.md) for the exact workflow, commands, permission boundaries and supporting references. Use the active agent workspace and verify actual outputs.
