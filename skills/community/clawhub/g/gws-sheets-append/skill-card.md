## Description:

Google Sheets: Append a row to a spreadsheet.

This skill is ready for commercial/non-commercial use.

## Publisher:

[googleworkspace-bot](https://clawhub.ai/user/googleworkspace-bot)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to append single or multiple rows to an intended Google Sheets spreadsheet through the gws CLI after confirming the spreadsheet ID, target range, and row values with the user.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can append data to a Google Sheets spreadsheet and may modify the wrong spreadsheet, tab, or range if inputs are incorrect.

Mitigation: Ask the user for confirmation before execution and verify the spreadsheet ID, target range, and row values.

Risk: The skill depends on the local gws CLI and the user's Google Workspace authentication context.

Mitigation: Install only a trusted gws CLI and use the shared gws authentication guidance before running append commands.

## Reference(s):

- [Gws Sheets Append on ClawHub](https://clawhub.ai/googleworkspace-bot/skills/gws-sheets-append)
- [googleworkspace-bot publisher profile](https://clawhub.ai/user/googleworkspace-bot)

## Skill Output:

**Output Type(s):** [shell commands, guidance]

**Output Format:** [Markdown with bash command examples and CLI flag guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the gws CLI and Google Workspace authentication context from the shared gws skill.]

## Skill Version(s):

1.0.13 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
