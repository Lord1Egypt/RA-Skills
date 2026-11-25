## Description:

用户指定 GPT Image 2.6 / 智慧模型2.6，制作 Temu、Shopee、TikTok Shop 或 Ozon 的多平台主图、铺货素材或本地化营销图时使用。Amazon 单独使用 2.6 亚马逊技能。按平台规范拆分任务并写好提示词，报价经用户确认后出图；没有 CLI 或密钥时交付可直接提交的出图方案。

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

Cross-border ecommerce sellers and creative operators use this skill to plan and generate localized product listing and marketing images for Temu, Shopee, TikTok Shop, and Ozon. It provides platform-specific prompts and submission-ready parameters when image generation is unavailable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs an unpinned third-party qhkit command-line package with the agent's permissions.

Mitigation: Where possible, pin and review the package version and limit the files and credentials available to it.

Risk: Generated listing images or copy could misstate product details or contain inaccurate localized text.

Mitigation: Check every image and text against the supplied product details before publishing; verify non-Latin copy with a translation tool or a fluent reviewer.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/autoagc/skills/linkpix-gpt-image-2-6-crossborder-image)

## Skill Output:

**Output Type(s):** [Images, Markdown, JSON, Shell commands]

**Output Format:** [Generated product images, or a Markdown image plan with JSON parameters and prompts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Tasks are separated by platform, purpose, and language; image generation is reported only when returned by the CLI.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
