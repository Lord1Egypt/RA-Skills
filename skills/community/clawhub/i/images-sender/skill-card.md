## Description: <br>
Send images from Mac to phone via iMessage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Wzyyyyyyyy](https://clawhub.ai/user/Wzyyyyyyyy) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to send local image files from a macOS machine to a configured phone number through the Messages app. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automatically send local images through the user's Mac Messages account. <br>
Mitigation: Review each requested recipient and image path before execution, and use an explicit phone number instead of relying on ambiguous defaults. <br>
Risk: Sent images are retained as copied files under ~/Pictures/openclaw-send. <br>
Mitigation: Periodically clear ~/Pictures/openclaw-send when images are sensitive or no longer needed. <br>
Risk: AppleScript input handling is weak for unusual characters in filenames or recipients. <br>
Mitigation: Use simple file paths and recipient strings until AppleScript escaping is improved. <br>


## Reference(s): <br>
- [Images Sender on ClawHub](https://clawhub.ai/Wzyyyyyyyy/images-sender) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and plain text status output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands target macOS Messages through osascript and copy sent images to ~/Pictures/openclaw-send.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact/_meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
