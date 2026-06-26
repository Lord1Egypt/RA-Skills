---
name: office-generator-py
description: Generate Office files with a bundled Python engine. Use when creating or exporting Word (.docx), Excel (.xlsx), or PowerPoint (.pptx) files from structured JSON, reports, meeting minutes, project plans, trackers, business briefs, or natural-language requirements that must be turned into Office documents.
---

# Office Generator Py

Generate Office files with the bundled engine under `scripts/engine/`.

## First run

Install Python dependencies into the bundled virtualenv:

```bash
python3 skills/office-generator-py/scripts/setup_engine.py
```

If you manage the environment yourself, you can point the wrapper at another Python binary with `OFFICE_GENERATOR_PYTHON=/path/to/python`.

## Quick workflow

1. Decide the output type: `docx`, `xlsx`, or `pptx`.
2. Prefer a built-in business template when it fits.
3. Write a UTF-8 JSON request file.
4. Run `scripts/generate_office.py`.
5. Return the produced file path.

## Entrypoints

Use `scripts/generate_office.py`.

- Standard mode: pass `--type` with a full JSON request file.
- Business mode: pass `--kind`, `--title`, `--input`, and `--out`.

## Built-in templates

### Word
- `word_work_report_v1`
- `meeting_minutes_v1`

### Excel
- `excel_data_tracker_v1`
- `project_plan_v1`

### PPT
- `ppt_business_brief_v1`
- `project_status_brief_v1`

## Built-in business kinds

- `word-report`
- `meeting-minutes`
- `excel-tracker`
- `project-plan`
- `ppt-brief`
- `project-status-brief`

## Commands

Standard mode:

```bash
python3 skills/office-generator-py/scripts/generate_office.py \
  --type docx \
  --input /absolute/path/request.json \
  --out /absolute/path/output.docx
```

Business mode:

```bash
python3 skills/office-generator-py/scripts/generate_office.py \
  --kind meeting-minutes \
  --title "Office 评审会纪要" \
  --purpose "内部存档" \
  --input /absolute/path/content.json \
  --out /absolute/path/meeting_minutes.docx
```

## Request shaping

If the user gives natural language only, convert it into JSON first.

For supported request formats and sample payloads, read `references/input-formats.md`.

## Output contract

- Success: stdout prints the generated file path.
- Failure: stderr prints the error; command exits non-zero.

## Notes

- Keep output paths absolute when possible.
- Prefer business mode for common document types.
- Use standard mode when the caller already has full `documentType/templateId/contentSpec` JSON.
