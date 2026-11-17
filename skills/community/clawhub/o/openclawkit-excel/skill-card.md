## Description:

Excel file operation toolkit for reading, writing, cleaning, merging, splitting, and reporting on spreadsheet data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wanghao20150901](https://clawhub.ai/user/wanghao20150901)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to guide automated Excel workbook creation, reading, cleaning, merging, sheet management, and report generation. It is suited to local spreadsheet workflows that need Python or command-line examples using pandas and openpyxl.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated commands or code may create or overwrite spreadsheet files on local paths.

Mitigation: Use a dedicated working directory, verify input and output paths, and keep backups of important workbooks before execution.

Risk: Dependency behavior can vary across pandas and openpyxl versions.

Mitigation: Install in an isolated environment and pin dependency versions for repeatable spreadsheet processing.

Risk: The interface is Chinese-only and some documented examples appear inaccurate or incomplete.

Mitigation: Review generated commands against the actual CLI options and validate outputs on noncritical sample files first.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wanghao20150901/skills/openclawkit-excel)
- [Publisher profile](https://clawhub.ai/user/wanghao20150901)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown or plain text with Python and shell snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide creation or overwriting of local spreadsheet files when the generated commands or code are executed.]

## Skill Version(s):

1.0.1 (source: server release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
