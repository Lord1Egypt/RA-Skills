## Description:

Access Google Drive from OpenClaw using either GOOGLE_SERVICE_ACCOUNT_KEY service-account JSON or a GOOGLE_OAUTH_REFRESH_TOKEN from the Google Drive OAuth connector.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jack-piplabs](https://clawhub.ai/user/jack-piplabs)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to search, list, inspect, download, export, upload, and create folders in Google Drive from an OpenClaw agent session.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can operate with broad Google Drive credentials.

Mitigation: Use least-privilege Google credentials and install only where broad Drive access is intended.

Risk: Untrusted service-account JSON can expose or redirect credential use.

Mitigation: Use only trusted service-account JSON files and keep credential material out of prompts, logs, and shared workspaces.

Risk: Upload and folder-creation commands can change shared Drive contents.

Mitigation: Require explicit confirmation before upload or folder creation, especially in shared drives or delegated Workspace environments.

Risk: Arbitrary OAuth scope selection can expand access beyond the intended task.

Mitigation: Restrict or remove arbitrary scope use and prefer the minimum Google Drive scope needed for the workflow.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jack-piplabs/skills/google-drive-service-account)
- [Google Drive API v3](https://www.googleapis.com/drive/v3)
- [Google OAuth Token Endpoint](https://oauth2.googleapis.com/token)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, json, files]

**Output Format:** [Markdown with inline shell commands; command output is typically JSON or downloaded/exported files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Google Drive credentials and Python 3; supports service-account or OAuth refresh-token authentication.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
