## Description:

Comprehensive spreadsheet creation, editing, and analysis with support for formulas, formatting, data analysis, visualization, and recalculation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wu-uk](https://clawhub.ai/user/wu-uk)

### License/Terms of Use:

Proprietary

## Use Case:

Agents use this skill to create, edit, analyze, format, visualize, and recalculate spreadsheet files such as .xlsx, .xlsm, .csv, and .tsv while preserving formulas and existing template conventions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Formula recalculation may persistently modify the user's LibreOffice macro profile and may overwrite or trust an existing Module1.xba.

Mitigation: Use formula recalculation only in a contained environment or after confirming that LibreOffice profile changes and workbook writes are acceptable.

Risk: Spreadsheet creation and editing can introduce incorrect formulas, misleading calculations, or broken workbook references.

Mitigation: Review generated workbooks, run the provided recalculation and error scan workflow, and resolve reported formula errors before relying on the output.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wu-uk/skills/jpg-ocr-stat-xlsx)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files, guidance]

**Output Format:** [Markdown guidance with inline Python and shell command examples; generated or modified spreadsheet files when used by an agent.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Spreadsheet outputs may include formulas, formatting, charts, workbook edits, and JSON-formatted recalculation reports.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
