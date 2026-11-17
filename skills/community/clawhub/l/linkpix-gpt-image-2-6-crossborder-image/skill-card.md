## Description:

用户指定 GPT Image 2.6 / 智慧模型2.6，制作 Temu、Shopee、TikTok Shop 或 Ozon 的多平台主图、铺货素材或本地化营销图时使用。Amazon 单独使用 2.6 亚马逊技能。

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

Cross-border e-commerce sellers and content operators use this skill to create localized product hero images and marketing assets for Temu, Shopee, TikTok Shop, and Ozon. It organizes work by marketplace, country site, and language, with checks for product consistency, localization, and generation cost.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reference images are uploaded to Qinghu during generation.

Mitigation: Use only reference images you are comfortable sharing with Qinghu.

Risk: A QHKIT_BASE_HOST override can change the API destination.

Mitigation: Check the configured site and API destination before generation.

Risk: Image generation incurs a cost.

Mitigation: Review the estimate and confirm before starting paid generation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/autoagc/skills/linkpix-gpt-image-2-6-crossborder-image)
- [Qinghu API Keys](https://www.iqinghu.com/workbench/dashboard/api-keys?urlCode=1788417429126)

## Skill Output:

**Output Type(s):** [Images, Shell commands, Configuration, Guidance]

**Output Format:** [Generated image files, JSON task parameters, shell commands, and a concise generation status report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Tasks can be grouped by marketplace, country site, and language; image prompts are limited to 5000 characters.]

## Skill Version(s):

0.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
