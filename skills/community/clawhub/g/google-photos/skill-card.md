## Description:

Manage Google Photos library content by listing albums, creating albums, and uploading photos through the Google Photos Library API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jorgermp](https://clawhub.ai/user/jorgermp)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to automate Google Photos album inspection, album creation, and photo uploads from an OpenClaw agent using their own Google OAuth credentials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: OAuth credentials and token files may be exposed or misused if stored insecurely or accepted from another source.

Mitigation: Use a dedicated Google OAuth client, keep credentials.json and token files in a private directory, and never use token files supplied by someone else.

Risk: The skill requests broader Google Photos authority than its listed commands need.

Mitigation: Prefer a version that removes the unused sharing scope and uses the narrowest Google Photos scopes required for list, create, and upload actions.

Risk: Pickle token storage can create unnecessary local token-handling risk.

Mitigation: Prefer a version that replaces pickle token storage with Google credential JSON and owner-only file permissions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jorgermp/skills/google-photos)
- [Google Photos Library API albums endpoint](https://photoslibrary.googleapis.com/v1/albums)
- [Google Photos Library API uploads endpoint](https://photoslibrary.googleapis.com/v1/uploads)
- [Google Photos Library API batchCreate endpoint](https://photoslibrary.googleapis.com/v1/mediaItems:batchCreate)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user-provided Google OAuth client credentials and local token storage.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
