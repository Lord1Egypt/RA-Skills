---
name: "GKTJ-Pt-skill"
description: "Use when generating patient-facing questionnaire analysis reports from uploaded survey spreadsheets or questionnaire tables, especially when the output must include fixed sections, consistent charts, controlled Word typography, and restrained patient-facing wording."
---

# GKTJ Patient Survey Report Generator

## Overview
This skill generates patient-facing questionnaire analysis reports with a fixed structure, controlled wording, and `.docx` output. The repository is currently migrating from a lightweight direct renderer toward a template-driven patient report workflow with fixed `.docx` templates and Word native editable charts.

## When to Use
- Uploaded attachment contains patient questionnaire data, especially `.xlsx`, `.csv`, or copied survey tables.
- Output must follow a fixed patient report structure rooted in:
  `引言` / `数据信息分析` / `反馈意见分析` / `附件`.
- Every question in chapter 2 needs a matching chart.
- The report must stay in patient viewpoint throughout.
- The user wants `.md` and `.docx` artifacts, not just chat output.

Do not use this skill for doctor reports, clinical trial manuscripts, or unstructured brainstorming.

## Workflow
1. Normalize inputs:
   - Required: `品种`, `地区`, questionnaire attachment.
   - Optional: `时间`, custom execution note, custom output directory.
2. Parse the questionnaire data first.
   - Use `scripts/parse_questionnaire.py` for spreadsheet inputs.
   - Save structured output as `questionnaire.json` before writing report sections.
3. Derive one statement-style title per question.
   - These titles are the chapter 2 dimension headings.
4. Generate report content in this order:
   - `引言`
   - `2、数据信息分析` question by question
   - `3.1 积极反馈`
   - `3.2 待改进反馈`
   - `4、附件-问卷题目内容`
   - When drafting prose, use the patient expression modules in `references/expression-modules.md`.
5. Build a report payload JSON through a script, not by hand.
   - AI should first write `report_content.md` or `report_content.jsonl`.
   - Use `scripts/build_payload.py` to convert that draft plus `questionnaire.json` into a valid `report_payload.json`.
6. Render artifacts.
   - Legacy path: use `scripts/render_report.py` to generate charts, markdown, docx, and a summary JSON.
   - Target path: fill a fixed `.docx` template and update template-native Word charts.
   - The template-driven rules live in `references/template-spec.md`.
7. Verify before delivery.
   - Chart count must equal chapter 2 question count.
   - Attachment must preserve original question and option meaning.
   - No absolute efficacy or safety claims.

## Required Output Rules
- Patient viewpoint only. Do not rewrite as doctor judgement.
- Do not invent sample size, hospitals, institutions, or dates.
- If sample size or time is missing, use restrained wording and omit unsupported facts.
- In chapter 2, analyze percentage relationships; do not mechanically enumerate A/B/C/D and stop there.
- In chapter 2, each question should preferentially use one of these 3 analysis angles:
  - analyze option percentages and give a conclusion plus feasible suggestion
  - analyze the percentage of major options one by one and explain possible causes
  - analyze the overall percentage structure and summarize the group-level pattern
- The model may randomly choose any one of the 3 angles question by question, but the chosen angle must still fit the actual data distribution.
- In chapter 2, always decide the pattern first, then write:
  - overall recognition
  - conditional recognition
  - behavioural split
  - pain-point attention
- Translate percentage structure into:
  patient experience, self-management behaviour, convenience, understanding, support needs.
- Do not turn patient questionnaire feedback into efficacy proof or clinical recommendation.

## Section Rules
- Read `references/section-rules.md` before generating text.
- Read `references/compliance-rules.md` before finalizing text.
- Read `references/execution-rules.md` before building the report payload.
- Read `references/expression-modules.md` before drafting narrative paragraphs.

## Scripts
- `scripts/parse_questionnaire.py`
  - Reads questionnaire spreadsheets and emits normalized JSON.
- `scripts/build_payload.py`
  - Reads `questionnaire.json` plus structured report content and emits a validated `report_payload.json`.
- `scripts/render_report.py`
  - Legacy renderer for the original lightweight flow.
  - Generates markdown, PNG charts, `.docx`, and a summary JSON.
  - This path is not the long-term solution for customer-template parity.
- `scripts/render_from_template.py`
  - Loads the fixed patient `.docx` template and writes structured payload v2 text back into the template.
- `scripts/update_word_charts.py`
  - Updates pre-seeded Word native editable charts inside the rendered `.docx`.

## Expected File Flow
- Input:
  - attachment spreadsheet
- Intermediate:
  - `questionnaire.json`
  - `report_content.md` or `report_content.jsonl`
  - `report_payload.json` or `report_payload.v2.json`
- Output:
  - `report_draft.md`
  - `report_final.md`
  - `charts/chart_XX.png` for legacy flow only
  - `report_rendered.docx` for template-driven flow
  - `问卷调研分析报告-{{品种}}-患者端-{{地区}}.docx`
  - `report_summary.json`

## Common Mistakes
- Writing in doctor viewpoint.
- Letting chapter 3 repeat chapter 2 item by item.
- Asking the model to handwrite a long `report_payload.json` with many Chinese paragraphs.
- Turning patient feedback into “证明疗效” or “安全性确证”.
- Forgetting that every chapter 2 item needs one chart and only one chart.
- Extending the legacy direct renderer when the request is really about the template-driven workflow.

## Final Delivery
Reply with:
- markdown final path
- docx path
- chapter completeness check
- chart count check
- chart style consistency check
- missing or uncertain data
- unresolved issues
