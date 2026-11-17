## Description:

Process Excel and PDF files by extracting data, parsing tables, and supporting report generation for .xlsx, .xls, .csv, and .pdf workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[laimiaohua](https://clawhub.ai/user/laimiaohua)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and operations users use this skill to process spreadsheets and PDFs, extract tabular or text content, convert Excel data to CSV, and prepare report outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Parsing untrusted Excel or PDF files can expose the runtime to malformed-document parser risks.

Mitigation: Install and run the skill only in an environment appropriate for untrusted document parsing.

Risk: Dependency versions are ranged rather than locked.

Mitigation: Use pinned or locked dependency versions for deployment.

Risk: Broad trigger wording and Chinese-only helper text may reduce predictable routing or English-facing usage.

Mitigation: Review routing descriptions and localize user-facing help before deploying where predictable English behavior is required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/laimiaohua/skills/gi-excel-pdf-process)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Files, Guidance]

**Output Format:** [Markdown guidance with Python and shell snippets; helper scripts emit CSV files or extracted PDF text and tables.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires local Python dependencies for pandas, openpyxl, and pdfplumber; no external service integration is described.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
