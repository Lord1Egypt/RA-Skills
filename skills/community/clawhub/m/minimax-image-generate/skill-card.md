## Description: <br>
MiniMax 图片生成技能 - 支持文生图(Text-to-Image)、图生图(Image-to-Image)。支持多种宽高比(1:1/16:9/9:16/4:3/3:4)，返回 URL 或 Base64 格式，可下载保存到本地。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[silingyuan0](https://clawhub.ai/user/silingyuan0) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to generate or edit images with MiniMax from text prompts or reference images. It can return generated image URLs or Base64 image data and save outputs to local files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and selected reference images are sent to MiniMax through its image generation API. <br>
Mitigation: Avoid submitting sensitive images or confidential prompts unless the deployment has approved MiniMax processing for that data. <br>
Risk: Generated images are written to user-specified local output paths. <br>
Mitigation: Save outputs in a dedicated folder and review output paths before execution to reduce accidental overwrites. <br>
Risk: The skill requires a MiniMax API key in the environment. <br>
Mitigation: Provide MINIMAX_API_KEY through a managed secret mechanism and avoid logging or committing credentials. <br>


## Reference(s): <br>
- [MiniMax Image API Reference](references/api.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/silingyuan0/minimax-image-generate) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, files] <br>
**Output Format:** [Text status messages, image URLs or Base64 image data, and saved image files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MINIMAX_API_KEY; URL responses are documented as valid for 1 hour.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
