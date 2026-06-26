## Description: <br>
Google Photos Library API integration with managed OAuth for uploading media, searching photos, creating and managing albums, and updating media items. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hith3sh](https://clawhub.ai/user/hith3sh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to connect an OpenClaw agent to Google Photos through ClawLink OAuth, then list albums and media, upload media, and manage albums or media metadata after confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires OAuth access to a connected Google Photos account through ClawLink. <br>
Mitigation: Review the Google account permissions during connection and install only when ClawLink is an acceptable hosted OAuth provider. <br>
Risk: The skill can upload media and change albums or media metadata. <br>
Mitigation: Confirm the target resource and intended effect before any upload, album change, or media update is executed. <br>
Risk: Google Photos Library API visibility is limited to media uploaded or created by this application. <br>
Mitigation: Use the Google Photos Picker API when the task requires access to the user's full photo library. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/hith3sh/google-photos-albums) <br>
- [Google Photos Library API Overview](https://developers.google.com/photos/library/guides/overview) <br>
- [Google Photos Media Items Reference](https://developers.google.com/photos/library/reference/rest/v1/mediaItems) <br>
- [Google Photos Albums Reference](https://developers.google.com/photos/library/reference/rest/v1/albums) <br>
- [Google Photos Picker API](https://developers.google.com/photos/picker) <br>
- [ClawLink Docs](https://docs.claw-link.dev/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API Calls, Configuration] <br>
**Output Format:** [Markdown with inline bash commands and JSON tool parameters] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read operations can return Google Photos album or media metadata; write operations require explicit user confirmation before execution.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
