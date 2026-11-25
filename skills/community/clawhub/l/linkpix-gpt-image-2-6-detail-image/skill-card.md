## Description:

用户指定 GPT Image 2.6 / 智慧模型2.6，制作电商详情页首图、卖点拆解图、参数信息图或可拼接的详情页长图时使用。按平台规范拆分任务并写好提示词，报价经用户确认后出图；没有 CLI 或密钥时交付可直接提交的出图方案。

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

面向电商运营者与商品内容创作者，用于把商品卖点、参数和使用场景整理成 GPT Image 2.6 详情页图片任务、提示词和可提交参数；环境可用且用户确认报价后可生成图片。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The qhkit CLI package is not version-pinned, and the security assessment has medium confidence with a partial scan.

Mitigation: Review and trust the package source, and verify the CLI version before installing or running it.

Risk: Generated product imagery or text may misstate product details or render copy inaccurately.

Mitigation: Use only confirmed product information, leave precise values blank for later overlay, and inspect each image before delivery.

Risk: Image generation may incur usage charges.

Mitigation: Show the estimate and obtain the user's explicit confirmation before generating images.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/autoagc/skills/linkpix-gpt-image-2-6-detail-image)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration, Guidance, Image files]

**Output Format:** [Markdown image plans and prompts, JSON parameters, and generated image files when generation succeeds]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [When image generation is unavailable, provides a ready-to-submit plan; image generation follows a quote and user confirmation.]

## Skill Version(s):

0.1.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
