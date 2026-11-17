## Description:

Converts JSON files to CSV by flattening nested objects and arrays for spreadsheet and analytics workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[albionaiinc-del](https://clawhub.ai/user/albionaiinc-del)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and data practitioners use this skill to convert JSON objects or lists into flattened CSV files for spreadsheets, reporting, and downstream analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Spreadsheet apps may interpret untrusted CSV values that begin with formula characters such as =, +, -, or @.

Mitigation: Use trusted JSON input or inspect and sanitize generated CSV output before opening it in spreadsheet software.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/albionaiinc-del/skills/json2csv)

## Skill Output:

**Output Type(s):** [text, shell commands, files]

**Output Format:** [Markdown usage guidance, shell commands, and generated CSV files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Flattens nested JSON keys with dot-separated paths and writes sorted CSV headers.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
