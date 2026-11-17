## Description:

Converts 电力交易/电网边界条件 96-point Excel data into 24 hourly averages by averaging each consecutive set of four 15-minute rows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mecyalika](https://clawhub.ai/user/mecyalika)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and power-trading operations users use this skill to convert 96-point Excel workbooks into auditable 24-point hourly result and formula sheets, or to repair existing templates with incorrect 24-point formula mappings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Converted spreadsheets or formulas from untrusted workbooks can carry spreadsheet-safety risk or incorrect formulas into downstream Excel workflows.

Mitigation: Use trusted source workbooks when possible, review generated formulas and numeric results before sharing outputs, and be cautious opening converted files from attacker-supplied spreadsheets.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mecyalika/skills/power-trading-96-to-24)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline Excel formulas, shell commands, and optional generated Excel workbook files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce source96, result24, and formula24 workbook sheets for auditability.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
