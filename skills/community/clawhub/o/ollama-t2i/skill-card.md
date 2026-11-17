## Description:

本地 Ollama 文生图工具。使用 x/z-image-turbo 模型生成图片，分辨率 1024x1024，每张图约耗时 90 秒。当用户说"生成图片"、"文生图"、"画一张图"、或提交中文提示词生成图像时使用。

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiafeimao-gjf](https://clawhub.ai/user/jiafeimao-gjf)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to generate local 1024x1024 images from Chinese text prompts through an Ollama-hosted x/z-image-turbo model. It supports single-prompt and multi-prompt image generation, saving generated PNG files to a local output directory.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts may contain sensitive information sent to the configured local Ollama service.

Mitigation: Do not include secrets or confidential data in image prompts, and confirm the local Ollama service is trusted before use.

Risk: Generated images are written to the default images directory or to the user-provided output path.

Mitigation: Run the skill from an appropriate working directory and review the output path before generating images.

Risk: The skill depends on the local x/z-image-turbo model and Ollama service matching the expected behavior.

Mitigation: Verify the installed model and local Ollama service before running the script.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jiafeimao-gjf/skills/ollama-t2i)
- [Publisher profile](https://clawhub.ai/user/jiafeimao-gjf)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Guidance]

**Output Format:** [PNG image files saved locally with terminal status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local Ollama at http://localhost:11434 with model x/z-image-turbo; default output directory is images/.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
