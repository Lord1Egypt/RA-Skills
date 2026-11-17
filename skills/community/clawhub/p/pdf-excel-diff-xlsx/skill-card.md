## Description:

Provides spreadsheet creation, editing, analysis, formatting, visualization, and formula recalculation workflows for files such as .xlsx, .xlsm, .csv, and .tsv.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lnj22](https://clawhub.ai/user/lnj22)

### License/Terms of Use:

Proprietary. LICENSE.txt has complete terms

## Use Case:

Employees, external users, and developers use this skill to create, modify, analyze, and verify spreadsheet workbooks while preserving formulas, formatting, and source documentation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The formula recalculation helper can persistently modify the user's global LibreOffice macro profile.

Mitigation: Review before installing or running; prefer an updated version that uses an isolated temporary LibreOffice profile, verifies any macro it invokes, and avoids overwriting existing macros.

Risk: The recalculation workflow saves workbook changes after running LibreOffice formula recalculation.

Mitigation: Run on a copy or confirmed target workbook, and ask before modifying existing workbooks or application configuration.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lnj22/skills/pdf-excel-diff-xlsx)
- [Publisher profile](https://clawhub.ai/user/lnj22)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files, guidance]

**Output Format:** [Markdown guidance with Python and shell snippets, generated spreadsheet files, and JSON formula-recalculation results.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May run LibreOffice to recalculate formulas and return workbook error summaries.]

## Skill Version(s):

0.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
