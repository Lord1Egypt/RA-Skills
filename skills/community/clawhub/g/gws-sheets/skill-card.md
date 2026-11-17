## Description:

Google Sheets: Read and write spreadsheets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[googleworkspace-bot](https://clawhub.ai/user/googleworkspace-bot)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to inspect Google Sheets CLI commands and build Google Sheets read, write, create, and metadata operations through the configured gws command.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide write-capable Google Sheets operations through the configured gws command.

Mitigation: Confirm the target spreadsheet, resource, method, and parameters before allowing changes.

Risk: The skill depends on the user's local Google Workspace CLI configuration and permissions.

Mitigation: Install and use it only where the configured gws account is intended to access the relevant Sheets data.

## Reference(s):

- [Google Sheets API field masks guide](https://developers.google.com/workspace/sheets/api/guides/field-masks)
- [Google Sheets API metadata guide](https://developers.google.com/workspace/sheets/api/guides/metadata)
- [ClawHub skill page](https://clawhub.ai/googleworkspace-bot/skills/gws-sheets)
- [ClawHub publisher profile](https://clawhub.ai/user/googleworkspace-bot)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline bash code blocks and command reference tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the gws binary and the user's configured Google Workspace CLI authentication.]

## Skill Version(s):

1.0.12 (source: server release evidence; skill metadata version 0.22.5)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
