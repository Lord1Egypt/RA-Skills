---
name: "mochi-expense-tracker"
description: "Import CSV transactions with deduplication, calculate exact totals and budgets, and export ledgers. Use for Expense Tracker and Budgets."
metadata: {"openclaw": {"requires": {"bins": ["node"]}, "homepage": "https://mochilab.bz", "version": "1.1.1"}}
---

# Expense Tracker and Budgets

## Build a verifiable household ledger

add records expense|income|refund with date, decimal amount, currency, category and description. Monetary arithmetic uses integer minor units; refunds reduce net expenses. Currencies stay separate. void retains a mistaken transaction and its reason. budget sets a category's monthly limit. Never infer actual bank transactions from vague chat.

## Import an actual CSV file

import-csv reads a workspace-relative UTF-8 file with kind,date,amount,currency,category and optional description,sourceId. Quoted commas and multiline fields are supported. A sourceId should be a stable bank/export transaction identifier; without it, the file hash and row position identify a reimport of the same file. The entire new batch is validated before saving. Duplicate keys are reported, not counted again. Invalid dates, amounts, currencies or malformed rows leave the existing ledger intact. The Skill reads user-supplied exports; it does not connect to a bank account.

## Reconcile totals and write a report

list and summary select an inclusive from/to range. They show income, expenses, refunds and category totals by currency. Budget spent values describe the whole budget month even when the selected range is shorter. export saves ledger.csv and budget-report.md with exact decimal amounts and remaining monthly budgets. Read the files and compare row counts with the import result. Missing data stays missing; a refund is not income. No currency conversion is performed.

## Run the local helper

Prepare an input JSON file inside the active agent workspace. Use the actual workspace, not another agent's directory.

```text
node "{baseDir}/scripts/run.mjs" --workspace "CURRENT_WORKSPACE" --input "request.json"
```

Read [references/input.md](references/input.md) before preparing fields. Every mutation and export uses a stable unique requestId; an identical retry returns its saved result. Put user text in JSON, not shell code. Successful exports return actual file paths, sizes and SHA256 values under this workspace's `.mochilab/mochi-expense-tracker/exports/` directory. Inspect the files before reporting completion. Previous exports are retained. No MochiLab key is needed by this standalone helper.

[User guide](README.md) · [Simplified Chinese guide](README.zh-CN.md)
