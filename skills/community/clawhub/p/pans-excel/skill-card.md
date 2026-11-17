## Description:

Pans Excel helps agents create, format, analyze, convert, and export Excel workbooks with charts, report templates, data validation, data cleaning, and CSV, JSON, and PDF workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dashiming](https://clawhub.ai/user/dashiming)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and agent users use this skill to generate and modify Excel workbooks, build business reports, add charts and validation, clean tabular data, and convert between XLSX, CSV, JSON, and PDF.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled Excel script can evaluate spreadsheet data input as Python code when JSON parsing fails.

Mitigation: Install only if the publisher is trusted, restrict how commands are invoked, and do not pass untrusted --data values.

Risk: Imported CSV or JSON data may contain spreadsheet formulas or other attacker-controlled cell content.

Mitigation: Avoid importing attacker-supplied CSV or JSON unless formula-like values are sanitized before conversion.

Risk: Formatting, charting, cleaning, validation, and autofmt commands can overwrite an existing workbook when no output path is provided.

Mitigation: Provide an explicit output path or work on a copy when modifying workbooks.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dashiming/skills/pans-excel)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands plus JSON or text command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands may create, modify, convert, or overwrite XLSX, CSV, JSON, and PDF files depending on output-path options.]

## Skill Version(s):

1.2.0 (source: server release metadata and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
