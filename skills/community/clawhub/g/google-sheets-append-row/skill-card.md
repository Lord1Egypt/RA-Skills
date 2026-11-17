## Description:

Atomic node skill to append a row in Google Sheets using the gog CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zvirb](https://clawhub.ai/user/zvirb)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill when they need to append a single row of values to a trusted Google Sheet range through the gog CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can modify Google Sheets data through a shell-style command.

Mitigation: Use only explicit, trusted spreadsheet IDs and ranges, confirm writes before execution, and prefer structured argument passing over shell interpolation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zvirb/skills/google-sheets-append-row)
- [Publisher profile](https://clawhub.ai/user/zvirb)

## Skill Output:

**Output Type(s):** [shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell command and JSON output expectation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the gog CLI and trusted Google Sheets spreadsheet IDs, ranges, and values.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
