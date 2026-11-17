## Description:

将用户照片转化为独立的 3:4 编辑风格海报，并提供简短的版式说明与生成提示词。

This skill is ready for commercial/non-commercial use.

## Publisher:

[yzfly](https://clawhub.ai/user/yzfly)

### License/Terms of Use:

MIT

## Use Case:

照片创作者可用此 skill 为每张上传照片制作一张简洁的编辑风格海报，保留照片上半部分，并在下半部分用几何色块、留白和精简文案重构主体。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Uploaded photos may contain private details that are sent to the selected image provider.

Mitigation: Use an image provider you trust and avoid uploading photos you are not comfortable sharing with it.

Risk: The optional global installation command skips prompts and installs changing dependencies.

Mitigation: Prefer reviewed dependency versions or use the documented manual installation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yzfly/skills/photo-window-poster)
- [Chinese image-generation prompt](artifact/references/prompt.zh-CN.md)
- [English image-generation prompt](artifact/references/prompt.en.md)

## Skill Output:

**Output Type(s):** [Images, Text, Guidance]

**Output Format:** [One 3:4 poster image per photo, with a short Markdown note and an image-generation prompt]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Each photo is delivered separately, without a collage; image creation requires a host with image editing or image-generation capability.]

## Skill Version(s):

1.0.0 (source: skill frontmatter and server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
