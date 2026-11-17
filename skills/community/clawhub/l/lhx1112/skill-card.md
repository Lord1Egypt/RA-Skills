## Description:

Comprehensive spreadsheet creation, editing, and analysis with support for formulas, formatting, data analysis, visualization, and formula recalculation for spreadsheet files such as .xlsx, .xlsm, .csv, and .tsv.

This skill is ready for commercial/non-commercial use.

## Publisher:

[goulonghui](https://clawhub.ai/user/goulonghui)

### License/Terms of Use:

Proprietary

## Use Case:

Developers and spreadsheet users use this skill to create, edit, analyze, format, and validate spreadsheet workbooks while preserving formulas and workbook conventions. It is especially suited for Excel workflows that need formulas, financial model formatting standards, pandas or openpyxl code, and LibreOffice-based recalculation checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The recalculation helper can make persistent changes to the user's LibreOffice profile by installing or updating a macro file.

Mitigation: Review before installation or execution, and prefer running recalc.py in an isolated LibreOffice profile or disposable environment when profile integrity matters.

Risk: Spreadsheet edits, formulas, and financial model assumptions can produce incorrect or misleading workbooks if references, input data, or formatting conventions are wrong.

Mitigation: Validate formulas with recalc.py, inspect reported spreadsheet errors, and review key assumptions, links, and formulas before relying on the workbook.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/goulonghui/skills/lhx1112)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell command snippets; spreadsheet files may be produced by following the generated code or workflow.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or modify spreadsheet files and may return JSON-formatted recalculation or formula-error results from recalc.py.]

## Skill Version(s):

1.0.12 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
