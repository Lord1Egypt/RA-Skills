## Description:

Personal protective equipment tracker. Use when json ppe tasks, csv ppe tasks, checking ppe status.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bytesagain3](https://clawhub.ai/user/bytesagain3)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams can use this skill to track PPE entries, check PPE status, search records, export data, and view simple statistics through a local CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review reports a command-execution flaw in the configuration command when used with untrusted values.

Mitigation: Review the skill before installation and use the config command only with trusted keys and values.

Risk: The remove and export commands can change or write local files.

Mitigation: Confirm the target data and working directory before removing records or exporting data.

Risk: Exported CSV data can be unsafe if opened in spreadsheet software when the data is untrusted.

Mitigation: Open exported CSV files only when the tracked PPE data is trusted.

## Reference(s):

- [BytesAgain](https://bytesagain.com)
- [Ppe on ClawHub](https://clawhub.ai/bytesagain3/skills/ppe)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Files]

**Output Format:** [Plain text CLI output, JSONL records, and optional JSON or CSV export files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores local PPE data under the configured PPE directory and may write export files in the working directory.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
