---
name: hr-workforce-dashboard
description: "Generate standardized HR workforce dashboards from Excel files: 5 fixed dashboards covering headcount trends, regional distribution, detailed breakdowns, attrition analysis, and contractor/partner distribution. Outputs a self-contained interactive HTML with ECharts charts, one-click email generation, and clipboard copy."
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - python3
    emoji: "📊"
---

# HR Workforce Dashboard

## Purpose

Generate a fixed-caliber workforce dashboard bundle from uploaded Excel attachments.
Produce up to 5 standard dashboards by default and allow optional user-requested add-on dashboards after the standard set.
Output a self-contained `dashboard.html` as the primary deliverable, with optional `ZIP` packaging containing `HTML + PNG + EXCEL + PPT`.

This skill is **not** a general BI builder. Treat dashboard definitions, field rules, BG mappings, regional scope, and attrition formulas as fixed business logic unless the user explicitly asks for a new custom dashboard in addition to the standard 5.

## When to Use

Trigger this skill when the user:
- uploads workforce Excel files and asks for `人力看板`、`看板`、`headcount dashboard`、`attrition dashboard`、`workforce report`
- asks to turn active / termination / contingent detail files into downloadable dashboards
- needs a packaged workforce output containing HTML, PNG, Excel, or PowerPoint
- mentions `看板` in the context of workforce data or HR reporting

## Required Inputs

Expect one or more Excel attachments.
Read only the first worksheet unless the user explicitly says otherwise.

### Attachment Structure

Three types of files are supported. File type is **always** determined from **row 1 content** (report name), never from the filename.

- **Active files (在职明细)**:
  - Rows 1-6 are metadata, row 7 is the header, row 8+ is data
  - Row 1: report name, fixed value `Overseas Active Employee Report`
  - Row 4: snapshot date in format `Effective Date | <date>` (A=label, B=date value)
  - Rows 2-3, 5, 6 are ignored
- **Termination files (离职明细)**:
  - Rows 1-7 are metadata, row 8 is the header, row 9+ is data
  - Row 1: report name, fixed value `Overseas Terminated Employee Report`
  - Row 4: start date in format `Termination Date From | <date>`
  - Row 5: end date in format `Termination Date To | <date>`
  - Rows 2-3, 6, 7 are ignored
- **Contingent Worker files (外包人员明细)**:
  - Row 1: report name containing `Contingent Worker` (e.g. `Overseas Contingent Worker Report`)
  - Row 2: header row
  - Row 3+: data rows
  - Data is always the latest snapshot; no snapshot_date metadata needed
  - Worker type is determined from `WeCom Name` prefix: `v_` → Contractor, `p_` → Partner
  - Country names are in Chinese; the script has a built-in Chinese → English + Region mapping

- **Never** infer file type from the filename
- Old metadata format (key=value in row 1) is **not** supported

### Required Data Fields

The formal table should contain these business fields when applicable:

**Active & Termination files:**
- `Employee Type`
- `Region`
- `WD Employee ID`
- `Country/Territory`
- `BG`
- `Hire Date`
- `Termination Date` (termination only)
- `Termination Category` (termination only)

**Contingent Worker files:**
- `HQ Employee ID` (or any column containing "Employee" and "ID")
- `WeCom Name` (used to classify Contractor vs Partner)
- `Country/Territory` (Chinese country names)
- `BG`

Apply `snapshot_date` from metadata rows, not from the filename.
Treat `Employee Type` as fixed enumerations: `Regular`, `Intern`.
Treat active files as active-only snapshots.
Treat termination files as the source for attrition statistics.
Treat contingent worker files as the latest snapshot for contractor/partner distribution.

## Execution Workflow

### 1. Prepare a Working Folder

Create a working directory inside the current workspace, for example:

```bash
mkdir -p workforce_dashboard_output
```

### 2. Review Reference Docs Before Running

Use these references while executing the task:
- `references/field_mapping.md`
- `references/metric_definitions.md`
- `references/layout_spec.md`

### 3. Run the Main Generator Script

Run the bundled script on every uploaded Excel attachment:

```bash
python3 "{skill_path}/scripts/build_dashboard_bundle.py" --files <file1.xlsx> <file2.xlsx> ... --output-dir workforce_dashboard_output
```

Optional arguments:
- `--bundle-name workforce_dashboard`
- `--title "人力数据看板"`

The script automatically classifies each file by reading row 1:
- Active → standard read (rows 1-6 meta, row 7 header)
- Termination → standard read (rows 1-7 meta, row 8 header)
- Contingent → dedicated reader (row 1 name, row 2 header, row 3+ data)

### 4. Review the Output Bundle

Verify that the output directory contains:
- `dashboard.html` (always generated — primary deliverable)

If full bundle mode is requested, also check:
- `png/dashboard_1.png` to `png/dashboard_4.png`
- `excel/workforce_dashboard.xlsx`
- `ppt/workforce_dashboard.pptx`
- `summary.md`
- `workforce_dashboard.zip`

### 5. Report Degraded Scenarios Clearly

If comparison months or attachment types are missing, do not stop unless the active snapshot input is entirely unavailable.
Continue generating all possible outputs and clearly mark incomplete sections as `数据不完整`.
Call out which months or dataset types are missing.
Remind the user that re-uploading missing files will produce a complete version.

## Fixed Dashboard Definitions

### Dashboard 1 — 正式员工趋势图

Generate a two-part trend view using **ECharts interactive grouped bar charts**:
- Left chart: same month last year vs latest month (同比)
- Right chart: latest three months month-over-month trend (环比)

Features:
- Interactive tooltip on hover showing detailed data
- Legend showing Americas / APAC / EMEA with region-specific colors
- "最新月份" annotation in top-right of MoM chart
- Dashed highlight rectangle on the latest month
- Bar labels showing headcount values on top
- Responsive resize on window change

Rules:
- count only `Employee Type = Regular`
- scope only `Americas`, `APAC`, `EMEA`
- use active snapshot files only
- latest month = latest uploaded active `snapshot_date`
- if last-year-same-month or recent months are missing, still generate and mark `数据不完整`

### Dashboard 2 — 期末在离职分析

Generate a latest-month regional distribution view with **ECharts interactive pie charts**:
- Left pie: active headcount by region (light blue background `#dfe8f1`)
- Right pie: YTD attrition by region (warm beige background `#eadccf`)

Features:
- Interactive tooltip on hover showing headcount and percentage
- Rich-text titles: "在职" highlighted in blue (`#1565C0`), "离职" highlighted in red (`#C62828`)
- Pie labels showing "Region\nN人 X%" inside each slice
- Responsive resize on window change

Rules:
- count only `Employee Type = Regular`
- scope only `Americas`, `APAC`, `EMEA`
- use latest active snapshot for active pie
- use termination detail within the calendar year for attrition pie
- show headcount and share for each region

### Dashboard 3 — Active Regular & Intern 明细汇总表

Generate the latest-month detailed headcount table.

Rules:
- region display order fixed as `Americas → APAC → EMEA → 海外合计 → Greater China → 海外合计（含试点国内）`
- sort countries within each region by total headcount descending
- show `Regular` and `Intern` for total and every fixed BG column group
- keep fixed BG display order from the reference docs

### Dashboard 4 — Attrition Regular 离职分析表

Generate the overseas attrition table.

Rules:
- count only `Employee Type = Regular`
- exclude `Mainland China`
- use termination detail rows whose `Termination Date` falls within the chosen period
- attrition rate formula:
  - `统计周期离职人数 / ((期初在职人数 + 期末在职人数) / 2) × 100%`
- show `Voluntary / Involuntary / Others`
- output by `Region → Country/Territory` with region subtotals

### Dashboard 5 — Active Contractor & Partner

Generate the overseas contingent worker distribution table. **Only produced when a Contingent Worker file is uploaded.**

Rules:
- classify workers by `WeCom Name` prefix: `v_` → Contractor, `p_` → Partner
- map Chinese country names to English using built-in mapping table (40+ countries)
- assign Region from the mapping table
- scope only `Americas`, `APAC`, `EMEA` (same as other dashboards)
- sort countries within each region by total worker count descending
- show `Contractor` and `Partner` sub-columns for total and every fixed BG column group
- use same BG display order as Dashboard 3: `合计 | IEG | CSIG | WXG | TEG | CDG | PCG | OFS | S1 | S2 | S3`
- include `海外合计` summary row
- table style matches Dashboard 3 (grouped header, region rowspan, same color scheme)

## Output Expectations

The primary deliverable is `dashboard.html` — a self-contained single-page HTML with:
- Inline CSS (from `assets/dashboard_style.css`)
- ECharts CDN (`echarts@5`) for interactive charts (Dashboard 1 & 2)
- ECharts interactive grouped bar charts for Dashboard 1 (tooltip, legend, responsive resize)
- ECharts interactive pie charts for Dashboard 2 (tooltip, rich-text titles, responsive resize)
- HTML tables for Dashboard 3, 4, 5 with all cell content centered (including Region column), and colspan=2 merge for summary rows ("海外合计" / "海外合计（含试点国内）")
- Interactive features (hover tooltips on charts, copy tables to clipboard)
- One-click email generation: copies full dashboard (with chart images) to clipboard and opens system email client with pre-filled subject and body. Email formatting: removes only Executive Summary title (keeps dashboard titles and footnotes title), uses `<table>` layout for horizontal chart arrangement (email clients don't support CSS flex), preserves table row/cell background colors, and table cell content is centered.
- Matplotlib PNG rendering preserved for Excel/PPT export use (fallback when ECharts data unavailable)

For full bundle mode, also package as a ZIP containing:
- `dashboard.html`
- `png/*.png`
- `excel/workforce_dashboard.xlsx`
- `ppt/workforce_dashboard.pptx`
- `summary.md`

Prefer mixed Chinese-English presentation:
- titles / notes / annotations in Chinese
- country, region, and BG names in English

## Installation and Quick Usage

### 安装方式

根据 CodeBuddy Skills 文档，这个 Skill 可以通过两种方式接入：

- **ZIP 导入安装**：在 CodeBuddy 设置页进入 Skill 管理区域，点击 **导入 Skill**，选择打包好的 `hr-workforce-dashboard.zip`
- **目录方式安装**：将 Skill 目录放到 `.codebuddy/skills/` 下进行本地开发或项目内调试

推荐：
- 对外分发使用 ZIP 导入
- 本地开发使用目录方式安装

### 快速使用

用户上传 Excel 附件后，可以直接这样触发：
- "请用这个 Skill 根据我上传的人力明细生成标准看板，并打包下载。"
- "请基于附件输出 HTML 看板。"
- "先按默认看板生成，再额外增加一个自定义看板。"

### 更多安装与使用示例

See `references/install_and_examples.md` for:
- detailed installation instructions
- trigger examples
- degraded-mode examples
- local script debugging example

## Notes for Reliable Use

- Prefer running the bundled script instead of rewriting the pipeline ad hoc
- Treat missing files as a degraded-mode reporting case, not a silent failure
- Preserve unknown BG values in the summary notes so users can extend the mapping later
- Append any user-requested custom dashboard **after** the standard 5 dashboards
- Dashboard 5 is conditional: only generated when contingent worker data is provided
