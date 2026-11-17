## Description:

Browse Google Drive folders and read the files inside them. Use when the user points at a Drive folder or file, asks for data stored in Drive (CSV/Excel/PDF exports, shared reports), or wants files organised, uploaded, or shared in Drive. Uses Composio for OAuth so no client-side Google credentials are needed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[berkgungor](https://clawhub.ai/user/berkgungor)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to browse, search, download, export, upload, organize, and share Google Drive files through a Composio-connected Google account. It is suited for workflows that need Drive file discovery, local analysis inputs, or Drive-based file publishing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can upload, move, trash, overwrite, and share Google Drive files.

Mitigation: Use a Drive account with limited access and require explicit user confirmation before share, move, trash, overwrite, upload, or broad permission changes.

Risk: Downloaded and exported Drive content can be written to local workspace paths.

Mitigation: Run the skill in a workspace where local file overwrites cannot affect important files and review destination paths before saving files.

Risk: The release evidence flags a disabled remote tool version safety check.

Mitigation: Pin the composio dependency and remove the remote tool version-check bypass before broad or unattended use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/berkgungor/skills/google-drive-composio)
- [Publisher profile](https://clawhub.ai/user/berkgungor)
- [Composio](https://composio.dev/)
- [Composio app](https://app.composio.dev/)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance, JSON, Files]

**Output Format:** [Markdown usage guidance with bash examples; CLI commands return JSON and may save Drive content as local files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires COMPOSIO_API_KEY, COMPOSIO_USER_ID or TENANT_ID, and the composio Python package.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
