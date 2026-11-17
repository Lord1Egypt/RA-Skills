## Description:

Google Drive API integration with managed OAuth. Search Drive files, manage permissions, organize folders, upload and download files, and handle sharing changes. Use this skill when users want to find, organize, share, or move files in Google Drive.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hith3sh](https://clawhub.ai/user/hith3sh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to connect an agent to a Google Drive account, discover files and folders, manage metadata and permissions, upload and download content, and perform confirmed Drive organization or deletion tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on a third-party hosted service and mutable plugin with broad Google Drive read/write authority.

Mitigation: Review the ClawLink publisher and plugin version before installing, confirm the granted Google OAuth scopes, and limit use with Drive accounts containing sensitive personal, business, or shared-drive data.

Risk: Write, sharing, trash, watch, and permanent-delete operations can alter access or remove Drive content.

Mitigation: Follow the skill's preview and explicit-confirmation workflow before every write or destructive operation, and verify the target file, folder, permission, or shared drive before execution.

Risk: The release has no server-resolved GitHub import provenance for this version.

Mitigation: Treat provenance as unavailable and evaluate the ClawHub release evidence, publisher profile, security verdict, and artifact contents directly before deployment.

## Reference(s):

- [ClawHub Google Drive skill page](https://clawhub.ai/hith3sh/skills/google-drive-files)
- [Google Drive API overview](https://developers.google.com/drive/api/v3/about)
- [Google Drive files resource](https://developers.google.com/drive/api/v3/reference/files)
- [Google Drive permissions resource](https://developers.google.com/drive/api/v3/reference/permissions)
- [ClawLink OpenClaw documentation](https://docs.claw-link.dev/openclaw)
- [ClawLink verification](https://claw-link.dev/verify)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, API calls, Configuration]

**Output Format:** [Markdown guidance with shell commands and JSON tool-call parameters]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses live Google Drive tool catalogs through ClawLink and requires explicit confirmation before write or destructive operations.]

## Skill Version(s):

1.0.5 (source: evidence.json release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
