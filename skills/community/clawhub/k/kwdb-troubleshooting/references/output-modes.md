# Output Modes

Default to the general diagnostic report.
Use the seven-section test-case template only when the user explicitly asks for a fixed seven-section report, a numbered incident sheet, or a test-case style output.

## Mode 1: General Diagnostic Report

Load `assets/general-diagnostic-template.md`.

Use when the user asks for diagnosis, root-cause analysis, log analysis, or performance diagnosis without naming a required template.

Rules:

- always reply in Chinese
- fill unknown items with `待补充`
- if source access is unavailable, section 4 must stop at the evidence conclusion
- if source access is available, section 4 may add source paths and the smallest useful call chain
- do not add recovery, mitigation, or reproduction plans

## Mode 2: Seven-Section Test-Case Template

Load `assets/output-template.md`.

Use only when the user explicitly asks for:

- a fixed seven-section output
- seven numbered headings
- a test-case sheet
- the existing numbered incident template

Rules:

- always reply in Chinese
- fill unknown items with `待补充`
- item 1 stays `待补充` unless history attribution was explicitly requested and supported
- item 4 stays blank unless the user already provided or explicitly confirmed reproduction steps
- item 7 holds the supporting evidence, and may include source paths or history notes when available
- do not invent recovery or reproduction content to satisfy the template

## Mode Selection Notes

- if the user does not mention a template, use Mode 1
- if the user asks for branch or commit tracing, keep the requested mode and extend only as far as the evidence supports
- if the requested template requires fields that cannot be justified yet, keep the format and mark them `待补充`
