## Description:

用户明确指定 GPT Image 2.6 / 智慧模型2.6，要做通用文生图、图生图、智能修图、创意插画或画质增强时使用。明确指定电商主图、白底图、场景图、投流图等用途时，优先使用对应的 2.6 专项技能。按平台规范拆分任务并写好提示词，报价经用户确认后出图；没有 CLI 或密钥时交付可直接提交的出图方案。

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

Designers, marketers, and other users can create general purpose images, illustrations, and image edits with GPT Image 2.6, or receive a ready-to-submit prompt and parameter plan when image generation is unavailable. The skill asks for confirmation of the price estimate before generating images.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review rated the release suspicious because its setup instructions use an unpinned CLI install or upgrade path; the scan was partial and its evidence is incomplete.

Mitigation: Review the CLI package and pin an exact version before use. Approve any installation or upgrade explicitly, and consider the skill's plan-only fallback.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/autoagc/skills/linkpix-gpt-image-2-6-generate)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration, Shell commands, Images]

**Output Format:** [Markdown guidance and prompts, JSON parameters, and generated image files when available]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Image generation requires an available CLI and credentials; otherwise the skill provides a ready-to-submit plan.]

## Skill Version(s):

0.1.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
