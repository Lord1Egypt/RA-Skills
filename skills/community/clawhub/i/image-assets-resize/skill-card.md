## Description:

直接以参考KV/海报/拍脸图为输入，调用 gpt-image-2 或 Nano Banana 模型，按目标规格批量生成精确尺寸的图片文件，交付前AI自检文字裁切、元素完整性等问题。支持自定义规范学习、产品设计语言积累。

This skill is ready for commercial/non-commercial use.

## Publisher:

[siconvip](https://clawhub.ai/user/siconvip)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing, design, and content teams use this skill to adapt a reference campaign image, poster, or face-oriented creative into correctly sized assets for multiple social and commerce platforms. Agents can run it to generate platform-specific PNG files, JSON result summaries, and optional base64 image payloads for cloud delivery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send user-provided marketing images and prompts to the configured image model provider or gateway.

Mitigation: Use only approved providers and avoid sensitive unreleased assets unless provider data handling has been reviewed.

Risk: API keys and base URLs are configurable, and plaintext API keys may be stored locally.

Mitigation: Prefer environment variables for credentials and avoid custom API base URLs unless they are trusted and controlled.

Risk: The optional GPT Image helper and upscaler installer can execute code outside the audited skill package.

Mitigation: Review those helpers before use and require approval before installing or running external helper code.

Risk: The skill may store sensitive configuration and brand history on the local system.

Mitigation: Keep local configuration and brand history files out of shared workspaces and remove sensitive campaign details when they are no longer needed.

## Reference(s):

- [Platform image specification reference](references/platform-specs.md)
- [OpenClaw ClawHub](https://github.com/openclaw/clawhub)
- [Real-ESRGAN ncnn Vulkan releases](https://github.com/xinntao/Real-ESRGAN-ncnn-vulkan/releases/download/)

## Skill Output:

**Output Type(s):** [Files, JSON]

**Output Format:** [JSON object with generated PNG output paths and optional base64 image data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated image files are saved to the configured output directory; cloud mode can include base64-encoded images in the JSON result.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
