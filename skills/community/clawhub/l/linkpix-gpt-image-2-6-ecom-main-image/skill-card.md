## Description:

用户指定 GPT Image 2.6 / 智慧模型2.6 制作商品首图、电商主图套图、轮播图或 SKU 图时使用。Amazon、抖音小店或其他跨境平台的明确需求走相应的 2.6 专项技能。

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

External ecommerce sellers and creative teams use this skill to prepare product hero images, carousel sets, and SKU images for requested marketplaces, using reference photos to retain product details.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: Reference images are sent to Qinghu for generation.

Mitigation: Use only images authorized for upload and verify the configured service destination before generation.

Risk: Image generation consumes paid credits.

Mitigation: Review the estimate and confirm the quoted credits before submitting generation requests.

Risk: The external CLI is installed globally without a fixed version and was not code-audited in the release evidence.

Mitigation: Check the installed CLI version and service configuration; use a reviewed, pinned CLI version where release assurance requires it.

## Reference(s):


## Skill Output:

**Output Type(s):** [Images, Shell commands, Configuration, Guidance]

**Output Format:** [Generated image files with JSON request files and command-line instructions.]

**Output Parameters:** [Variable by marketplace, SKU, image role, and requested image count.]

**Other Properties Related to Output:** [Generation includes an estimate and user confirmation before paid image creation.]

## Skill Version(s):

0.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
