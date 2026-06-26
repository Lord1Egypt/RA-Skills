## Description: <br>
给截图添加渐变背景和圆角，让分享更美观。当用户发送图片并说"美化"、"美化一下"、"加个背景"时触发。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[maoruibin](https://clawhub.ai/user/maoruibin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to turn a supplied screenshot into a shareable PNG with a gradient background, rounded corners, and optional bottom text. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill writes a new PNG beside the input image by default. <br>
Mitigation: Confirm the intended output location or provide an explicit output path before running it on user-supplied screenshots. <br>
Risk: Casual requests such as "beautify" or "add a background" may not clearly authorize this specific local image transformation. <br>
Mitigation: Confirm the user wants this beautifier before running it when the request is ambiguous. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/maoruibin/gudong-beautify-shot) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, files, guidance] <br>
**Output Format:** [PNG image file path with optional Markdown guidance and inline shell commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes a new PNG beside the input image by default; supports optional output path and bottom text.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
