## Description:

基于一张商品图快速生成多种营销版本，支持不同背景、布局和设计风格，轻松量产广告素材。当用户要求一张图出多个版本、图片裂变、素材裂变、量产不同风格的商品图时必须触发。关键词：LinkPix、qhkit、图像裂变、图片裂变、素材裂变、一图多版、批量版本、风格变体、广告素材量产、A/B测试素材。

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

E-commerce marketers and creative teams use this skill to turn a product image into multiple background, layout, and style variations for advertising and A/B testing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Product images are uploaded to an image service, and generation can consume account credits.

Mitigation: Use images you are comfortable uploading and check the estimated credit cost before large generation jobs.

Risk: Requests depend on an API token and the intended account and site configuration.

Mitigation: Protect the API token and confirm the account and site before running image-generation commands.

Risk: The security assessment covers the supplied Markdown and does not establish the safety of future npm package releases.

Mitigation: Review package versions and upgrade commands before installing or upgrading qhkit.

## Reference(s):

- [ClawHub release](https://clawhub.ai/autoagc/skills/linkpix-image-variations)
- [qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)

## Skill Output:

**Output Type(s):** [Images, Guidance, Shell commands]

**Output Format:** [Generated image variations and Markdown guidance with JSON-formatted command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Image variations can change product details; review text, logos, and product structure in generated images.]

## Skill Version(s):

0.1.8 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
