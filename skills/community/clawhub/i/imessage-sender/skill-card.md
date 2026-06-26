## Description: <br>
Send images from Mac to phone via iMessage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Wzyyyyyyyy](https://clawhub.ai/user/Wzyyyyyyyy) <br>

### License/Terms of Use: <br>


## Use Case: <br>
OpenClaw users on macOS use this skill to send a local image file to a phone number through the Messages app, either automatically when requested or through the provided command. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automatically send local images through the user's Mac Messages account. <br>
Mitigation: Confirm the recipient and image path before each send, and install only when this Messages behavior is intended. <br>
Risk: Copied images remain in ~/Pictures/openclaw-send/ and may contain sensitive content. <br>
Mitigation: Periodically clear ~/Pictures/openclaw-send/ when sent images should not be retained. <br>
Risk: Unusual characters in filenames or phone numbers may affect AppleScript handling. <br>
Mitigation: Avoid unusual characters in image paths and recipient values until AppleScript escaping is fixed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/Wzyyyyyyyy/imessage-sender) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses macOS Messages through AppleScript and copies images to ~/Pictures/openclaw-send/ before sending.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
