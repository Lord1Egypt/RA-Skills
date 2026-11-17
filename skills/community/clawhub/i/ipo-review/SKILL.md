---
name: ipo-review
description: 复核IPO申报材料（招股说明书、问询回复、财务报表附注等），运行本地IPO复核工具并解读报告。Use when Codex needs to review IPO filing materials for financial-data consistency, cross-file differences, table arithmetic checks, evidence locations, or report interpretation. The tool runs locally and does not upload files.
---

# IPO申报材料复核

Use this skill when the user asks to review IPO filing materials, inquiry responses, prospectuses, audit reports, financial-statement notes, or related disclosure files.

## Bundled Tool Location

This skill is self-contained when installed under Codex user skills. The bundled tool directory is the skill folder itself:

```text
%USERPROFILE%\.codex\skills\ipo-review
```

If the current working directory contains `main.py`, `src/`, and `config/`, use the current directory as the tool project. Otherwise, use this skill folder as the tool project. Do not rely on the original desktop development folder being present.

## Preflight

1. Confirm the selected tool project contains:
   - `main.py`
   - `src/`
   - `config/`
   - `input/`
   - `output/`
2. Confirm `input/` contains materials to review. Supported formats are PDF, DOCX, XLSX, and TXT.
3. If dependencies are missing during execution, install from the tool project with:

```bash
pip install -r requirements.txt
```

The review program itself must run locally. Do not upload source materials or call external APIs.

## Run

From the selected tool project directory, execute:

```bash
python main.py
```

The program reads `input/`, writes `output/`, and generates:

```text
output/IPO问询回复复核分析报告.html
output/issues.json
output/financial_facts.csv
output/evidence_index.json
output/comparison_exclusions.csv
output/arithmetic_skips.csv
output/parse_errors.csv
output/run_log.txt
```

## Report Interpretation

After running, read `output/issues.json` and `output/run_log.txt`.

Prioritize issues where:

```text
review_priority == "key"
```

These are the "待人工复核（重点）" items. For each key item, summarize:

- issue id, category, level, and priority;
- source files and evidence positions;
- source values and original text snippets when available;
- conclusion, caliber analysis, and suggested manual check;
- whether the item is likely a real issue or a candidate requiring manual confirmation.

For `review_priority == "normal"` and `review_priority == "noise"`, provide counts and category summaries by default. Expand details only if the user asks.

## Diagnostics

Use these files for quality checks:

- `comparison_exclusions.csv`: facts not compared and why.
- `arithmetic_skips.csv`: tables skipped for arithmetic checks and why.
- `parse_errors.csv`: real parsing failures.
- `financial_facts.csv`: extracted facts, units, periods, scopes, and metrics.
- `evidence_index.json`: paragraph/table-cell evidence locations.

When assessing whether the tool is reliable, check:

- whether parse errors are zero or explainable;
- whether key issues are few enough for manual review;
- whether high-priority items have usable evidence locations;
- whether obvious noise is labeled `noise` instead of `key`.

## Required Caveats

Always tell the user:

- This is a review assistant, not a substitute for professional judgment.
- It is strongest at numeric checks: cross-file values, units, periods, and table arithmetic.
- It does not understand all narrative or semantic contradictions.
- "No issue reported" does not mean the filing is confirmed correct.
- The user should still perform manual reading and professional review.

Do not overstate certainty. Do not describe unreported areas as verified.
