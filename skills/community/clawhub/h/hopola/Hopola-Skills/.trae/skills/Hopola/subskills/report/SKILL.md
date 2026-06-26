---
name: "hopola-report"
description: "Builds a unified Markdown delivery report. Invoke when pipeline or stage execution needs readable output."
---

# Hopola Report

## Purpose
Assemble search, generation, and upload outputs into a standard Markdown report.

## Trigger
- Output final delivery after full pipeline execution.
- Generate a standalone report in stage mode.

## Inputs
- `search_result`
- `generation_result`
- `upload_result`
- `errors`
- `response_language`

## Output
- `markdown_report`

## Rules
- Required sections: search summary, generation outputs, upload results, security alerts, and conclusion with next steps.
- For failures, always show failed stage, root cause, retry conclusion, and next recommendation.
- If `403001` is returned, include `redirect_url`.
- Language must follow `response_language`; if missing, infer from latest user message.
- Never default to Chinese; only use Chinese when the user language is Chinese.
- Rewrite any upstream mixed-language text into one consistent target language before final output.
