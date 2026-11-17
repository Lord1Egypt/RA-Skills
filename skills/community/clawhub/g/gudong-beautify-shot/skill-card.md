## Description:

给截图添加渐变背景和圆角，让分享更美观。当用户发送图片并说"美化"、"美化一下"、"加个背景"时触发。

This skill is ready for commercial/non-commercial use.

## Publisher:

[maoruibin](https://clawhub.ai/user/maoruibin)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn a single screenshot into a share-ready PNG with a gradient background, rounded corners, and optional bottom caption text.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Large or untrusted images can create ordinary image-processing reliability or resource-use risk.

Mitigation: Install in an isolated environment, pin Pillow when reproducibility matters, and apply resource limits before processing very large or untrusted images.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/maoruibin/skills/gudong-beautify-shot)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Guidance]

**Output Format:** [PNG image file path with optional text or markdown response]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Processes one input image at a time; supports optional bottom caption text and does not support custom color palettes or batch processing.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
