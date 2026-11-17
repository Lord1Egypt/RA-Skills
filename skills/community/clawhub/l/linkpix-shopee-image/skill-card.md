## Description:

帮助 Shopee 卖家和东南亚电商运营人员生成商品主图套图、详情长图及促销海报，并适配不同站点的视觉和语言需求。

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

Shopee sellers and Southeast Asian ecommerce operators use this skill to create product image sets, long-form detail images, and promotional artwork for marketplace listings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to provide API keys through chat and recommends automatic installation and updates of external software.

Mitigation: Configure API keys locally and rotate any key already shared; require approval for installations and upgrades, and use reviewed dependency versions.

Risk: Image generation uploads product images and can consume account credits.

Mitigation: Upload only intended product images and check the quoted credit cost before generation.

## Reference(s):

- [ClawHub release](https://clawhub.ai/autoagc/skills/linkpix-shopee-image)
- [qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)

## Skill Output:

**Output Type(s):** [Images, Guidance, Shell commands]

**Output Format:** [Generated image files or URLs with Markdown guidance and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Product image assets with optional platform-specific sizing, model selection, and localized promotional copy.]

## Skill Version(s):

0.1.4 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
