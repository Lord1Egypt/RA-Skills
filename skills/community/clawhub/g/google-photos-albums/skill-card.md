## Description:

Google Photos Library API integration with managed OAuth. Upload media, search photos, create and manage albums, and update media items. Use this skill when users want to manage their Google Photos library, create albums, or upload media.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hith3sh](https://clawhub.ai/user/hith3sh)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to manage Google Photos albums and media through ClawLink-managed OAuth, including listing, searching, uploading, creating albums, and updating media metadata.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses ClawLink-managed OAuth and tool calls for access to a connected Google Photos account.

Mitigation: Review the Google account permissions during connection, install only if you trust ClawLink and the ClawHub plugin source, and revoke the Google or ClawLink connection when it is no longer needed.

Risk: Write operations can create albums, upload media, add items, or update media descriptions.

Mitigation: Confirm the target resource and intended effect before each write operation, and preview upload, album, or media update calls before execution.

Risk: Google Photos Library API access is limited to media items uploaded or created by this application.

Mitigation: Use the Google Photos Picker API instead when the user needs access to photos created by camera uploads or other applications.

## Reference(s):

- [Google Photos Library API Overview](https://developers.google.com/photos/library/guides/overview)
- [Google Photos Media Items Reference](https://developers.google.com/photos/library/reference/rest/v1/mediaItems)
- [Google Photos Albums Reference](https://developers.google.com/photos/library/reference/rest/v1/albums)
- [Google Photos Picker API](https://developers.google.com/photos/picker)
- [ClawLink OpenClaw Documentation](https://docs.claw-link.dev/openclaw)
- [ClawLink Verification](https://claw-link.dev/verify)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON tool-call examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide authenticated Google Photos read and write tool calls after user connection and confirmation.]

## Skill Version(s):

1.0.6 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
