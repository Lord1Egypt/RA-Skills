## Description:

Read, write, append, and manage Google Sheets via the Google Sheets API (Node.js SDK). Use when you need to interact with spreadsheets - reading data, writing/updating cells, appending rows, clearing ranges, formatting cells, managing sheets. Requires a Google Cloud service account with Sheets API enabled.

This skill is ready for commercial/non-commercial use.

## Publisher:

[longmaba](https://clawhub.ai/user/longmaba)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to automate Google Sheets tasks such as reading ranges, writing or appending rows, formatting cells, adjusting sheet layout, and managing sheet tabs through a Node.js CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a Google service-account key with spreadsheet read/write access.

Mitigation: Store the key outside the skill directory when possible, keep it out of source control, limit spreadsheet sharing to the minimum required access, and rotate or revoke the key if exposed.

Risk: Commands such as clear and deleteSheet can remove spreadsheet data or sheet tabs.

Mitigation: Review destructive commands before execution and confirm the target spreadsheet ID, sheet name, and range for important sheets.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/longmaba/skills/google-sheet)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, JSON, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON arguments; CLI commands return JSON or text results from Google Sheets operations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Google Cloud service account with the Google Sheets API enabled and access to the target spreadsheets.]

## Skill Version(s):

1.0.0 (source: package.json and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
