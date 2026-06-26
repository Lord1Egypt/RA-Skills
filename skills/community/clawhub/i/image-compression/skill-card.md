## Description: <br>
Automatically compresses images above Telegram's 10 MB limit by resizing width, adjusting quality, and preserving the original file with a new compressed copy. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yeholdon](https://clawhub.ai/user/yeholdon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill on macOS to reduce large image files before sending them through messaging workflows such as Telegram or WeChat. It is useful when preserving the original image while creating a smaller platform-compatible copy matters. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Send helpers can immediately upload a user-selected image to Telegram or WeChat. <br>
Mitigation: Use the compression-only script for local resizing, and verify the image path, recipient, account, and destination before running any send helper. <br>
Risk: The WeChat helper calls a hard-coded local WeChat script that is outside this artifact. <br>
Mitigation: Avoid the WeChat helper unless the local script has been inspected and trusted on the executing machine. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yeholdon/image-compression) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, guidance] <br>
**Output Format:** [Markdown with inline bash commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local image paths for compressed files and may invoke send helpers when the user chooses a messaging workflow.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
