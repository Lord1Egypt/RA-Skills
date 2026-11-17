## Description:

Google Drive: Upload a file with automatic metadata.

This skill is ready for commercial/non-commercial use.

## Publisher:

[googleworkspace-bot](https://clawhub.ai/user/googleworkspace-bot)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators working with Google Workspace use this skill to have an agent prepare Google Drive upload commands for a named local file, optionally targeting a parent folder or custom filename.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill issues a Google Drive write command that can upload a local file to the wrong account, folder, or filename if executed without confirmation.

Mitigation: Confirm the selected file, destination folder, target filename, authenticated account, and user intent before running the upload command.

Risk: The skill depends on the external gws CLI and companion Google Workspace authentication instructions.

Mitigation: Install and trust the gws CLI, then review the generated or companion gws-shared instructions for authentication and security rules before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/googleworkspace-bot/skills/gws-drive-upload)
- [Publisher profile](https://clawhub.ai/user/googleworkspace-bot)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the gws CLI and prior Google Workspace authentication.]

## Skill Version(s):

1.0.12 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
