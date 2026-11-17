## Description:

Generates high-quality images from text prompts using the ZhiPu GLM-Image API, with controls for model, size, quality, watermarking, user ID, and optional local saving.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jaredforreal](https://clawhub.ai/user/jaredforreal)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and creative teams use this skill to ask an agent to generate AI images, illustrations, concept art, portraits, social media graphics, and posters through the ZhiPu GLM-Image API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and optional user IDs are sent to ZhiPu when using the GLM-Image API.

Mitigation: Avoid sensitive prompts or identifying user IDs, and use a dedicated API key with limited exposure.

Risk: The optional save feature downloads an API-provided image URL without enough validation or size limits.

Mitigation: Save only to non-critical new filenames until stricter download validation and overwrite protection are available.

## Reference(s):

- [GLM-Image skill homepage](https://github.com/zai-org/GLM-Image/tree/main/skills/glm-image-gen)
- [ZhiPu image generation API documentation](https://docs.bigmodel.cn/api-reference/%E6%A8%A1%E5%9E%8B-api/%E5%9B%BE%E5%83%8F%E7%94%9F%E6%88%90)
- [GLM-Image model documentation](https://docs.bigmodel.cn/cn/guide/models/image-generation/glm-image)
- [ZhiPu API key management](https://bigmodel.cn/usercenter/proj-mgmt/apikeys)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return temporary image URLs, content filter metadata, and an optional saved image file path.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
