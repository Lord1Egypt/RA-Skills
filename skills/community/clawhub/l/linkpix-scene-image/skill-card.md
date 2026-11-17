## Description:

根据商品自动生成真实、高质感的商品场景图，适用于家居、美妆、服饰、数码等行业。当用户要求生成商品场景图、使用场景展示图、氛围图、生活方式图（lifestyle）时必须触发。关键词：LinkPix、qhkit、场景图、商品场景、使用场景、氛围图、lifestyle、生活方式图、实景图、家居场景、美妆场景、点击率、转化率。

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

E-commerce sellers and marketing teams use the skill to create lifestyle and in-use product images for listings and advertising.

### Deployment Geography for Use:

China (the skill directs users to the domestic iqinghu.com service).

## Known Risks and Mitigations:

Risk: Installation and upgrade instructions include global software changes and recommend acting on returned upgrade commands.

Mitigation: Review each command and its source before running it, and keep installation and upgrades under your control.

Risk: Product images are sent to iqinghu.com for processing; the external CLI code and image-retention behavior were not verified.

Mitigation: Upload only images approved for external processing, and review the provider's data-handling terms before submitting sensitive imagery.

Risk: Generated images may slightly alter product text, logos, or structure.

Mitigation: Check those details against the source product image before using generated images in listings or advertising.

## Reference(s):

- [qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)
- [LinkPix scene image skill on ClawHub](https://clawhub.ai/autoagc/skills/linkpix-scene-image)

## Skill Output:

**Output Type(s):** [Images, Guidance]

**Output Format:** [Generated product-scene images with accompanying prompt and usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Image count can be set to 1, 2, 4, 6, 8, or 10; generated images may slightly change product details.]

## Skill Version(s):

0.1.8 (source: server-resolved ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
