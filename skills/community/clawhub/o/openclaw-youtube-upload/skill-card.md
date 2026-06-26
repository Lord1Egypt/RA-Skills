## Description: <br>
Uploads a video to YouTube using the official YouTube Data API v3 and OAuth 2.0, with support for titles, descriptions, privacy settings, and large file chunking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[BrOrlandi](https://clawhub.ai/user/BrOrlandi) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to upload selected video files to a chosen YouTube account through the YouTube Data API, including setting metadata and privacy status. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses Google OAuth credentials and creates a reusable local token for YouTube upload access. <br>
Mitigation: Keep client_secret.json and token.pickle private, do not commit them to source control, and revoke access or delete token.pickle when reusable upload permission is no longer wanted. <br>
Risk: An agent can upload a selected video with a public, private, or unlisted privacy setting. <br>
Mitigation: Confirm the file path, title, description, and privacy setting before each upload, especially before public uploads. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/BrOrlandi/openclaw-youtube-upload) <br>
- [README](README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, Text] <br>
**Output Format:** [Markdown with inline shell commands and status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python 3, pip3, Google OAuth client credentials, and a user-approved YouTube upload token.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
