## Description:

Uploads a video to YouTube using the official YouTube Data API v3 and OAuth 2.0, with support for titles, descriptions, privacy settings, and large file chunking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brorlandi](https://clawhub.ai/user/brorlandi)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill to upload local video files to YouTube through OAuth-backed YouTube Data API access, including setting titles, descriptions, and public, private, or unlisted visibility.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reusable OAuth credentials can allow later YouTube uploads without another browser approval while token.pickle remains present.

Mitigation: Use the skill only in a trusted private directory, delete token.pickle when finished, and revoke the app in the Google account when access is no longer needed.

Risk: Unsafe pickle deserialization of the local token file creates a local code execution risk if the file is replaced or modified.

Mitigation: Replace pickle token storage with JSON or an OS keyring and apply private file permissions to any local credential material.

Risk: Unpinned Python dependencies can change behavior or introduce vulnerable versions over time.

Mitigation: Pin dependency versions and review updates before installing or running the upload workflow.

Risk: The skill performs account-affecting uploads to YouTube.

Mitigation: Require explicit user approval before each upload and confirm the selected title, description, video file, and privacy setting.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/brorlandi/skills/openclaw-youtube-upload)
- [Publisher profile](https://clawhub.ai/user/brorlandi)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and plain-text upload status]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create a local token.pickle file and perform YouTube uploads after OAuth approval.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
