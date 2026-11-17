## Description:

Google Sheets: Read values from a spreadsheet.

This skill is ready for commercial/non-commercial use.

## Publisher:

[googleworkspace-bot](https://clawhub.ai/user/googleworkspace-bot)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Google Workspace users use this skill to have an agent read a specified range from a Google Sheets spreadsheet through the gws CLI without modifying the spreadsheet.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read Google Sheets data from any spreadsheet ID and range the user supplies.

Mitigation: Install and run it only when the agent should have read access to the specified spreadsheet data.

Risk: Authentication and global security behavior are delegated to the shared gws auth skill and gws CLI configuration.

Mitigation: Review the shared gws auth skill and CLI configuration before use.

## Reference(s):

- [Gws Sheets Read on ClawHub](https://clawhub.ai/googleworkspace-bot/skills/gws-sheets-read)
- [googleworkspace-bot publisher profile](https://clawhub.ai/user/googleworkspace-bot)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the gws CLI; the read command requires spreadsheet and range arguments.]

## Skill Version(s):

1.0.13 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
