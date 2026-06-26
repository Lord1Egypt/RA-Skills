## Description: <br>
Manage Google Photos library. Upload photos, create albums, and list library content. Use when the user wants to backup, organize, or share images via Google Photos. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jorgermp](https://clawhub.ai/user/jorgermp) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to let an OpenClaw agent upload photos, create albums, and list album information in Google Photos using their own Google OAuth credentials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires Google OAuth access to a user's Google Photos account. <br>
Mitigation: Use personal Google OAuth credentials, review the consent scopes before authorizing, keep credentials.json and token.pickle private, and revoke access when the skill is no longer needed. <br>
Risk: The upload action can send selected local image files to Google Photos or a specified album. <br>
Mitigation: Review the photo path and album ID before running upload commands, and upload only files intended for the target Google Photos library. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/jorgermp/google-photos) <br>
- [Google Photos Library API service](https://photoslibrary.googleapis.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, API calls] <br>
**Output Format:** [Markdown guidance with shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user-supplied Google OAuth credentials and a local token file.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
