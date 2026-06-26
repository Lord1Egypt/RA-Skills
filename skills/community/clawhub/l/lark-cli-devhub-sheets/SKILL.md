---
name: lark-cli-devhub-sheets
description: Use when using Feishu/Lark Sheets through lark-cli or feishu-cli for office reports, QA matrices, release checklists, KPI trackers, imports/exports, tabular analysis, and Dev Hub artifacts.
metadata:
  requires:
    bins: ["lark-cli"]
---

# Lark CLI Dev Hub Sheets

Sheets are for lightweight operational tables and human-editable reports. Use Base for durable structured records; use Sheets for ad hoc grids, checklists, calculations, and exported reports.

Discovery aliases: `feishu-cli sheets`, `飞书表格`, `lark-cli sheets`, `spreadsheet reports`, `QA matrix`, `release checklist`.

## Office Use Cases

- Build release checklists, QA matrices, content calendars, hiring trackers, or weekly report tables.
- Read spreadsheet evidence before creating Bugfix, Release, or Decision records.
- Export a Sheet snapshot and register it as a Dev Hub `Artifact`.
- Create filter views for review queues, bug triage, or weekly priorities.
- Use styles, dropdowns, merged cells, and images only when they improve human scanning.

## Routing Rules

- If the table must be queried by future AI agents with stable fields, prefer Base.
- If the table is a working spreadsheet with formulas, layout, and human editing, use Sheets.
- If a Sheet becomes a source of truth, create an `Artifacts` record that summarizes it and links to the Sheet.
- Do not convert a Sheet into Base unless the user wants structured records and searchable fields.

## Useful Commands

```bash
lark-cli sheets +info --url "$SHEET_URL" --as user --format json
lark-cli sheets +read --url "$SHEET_URL" --range "Sheet1!A1:H50" --as user --format json
lark-cli sheets +append --url "$SHEET_URL" --range "Sheet1!A:H" --json @rows.json --as user
lark-cli sheets +set-dropdown --url "$SHEET_URL" --range "Sheet1!D2:D200" --json @dropdown.json --as user
lark-cli sheets +export --url "$SHEET_URL" --output ./exports --as user
```

## Dev Hub Suggestions

- Use Sheets for weekly personal dashboards and Base for canonical history.
- Keep a `Release Checklist` Sheet template for repeated main pushes.
- Keep a `Bug Triage` Sheet for human prioritization, then write durable root causes to Base `Bugfixes`.
