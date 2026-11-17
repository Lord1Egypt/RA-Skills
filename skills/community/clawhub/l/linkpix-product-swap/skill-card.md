## Description:

一键替换图片中的商品主体，自动保留场景、构图及光影效果，大幅提升商品素材复用效率。当用户要求把图里的商品换成另一个商品、场景图复用给新品、替换产品主体时必须触发。关键词：LinkPix、qhkit、产品替换、商品替换、换商品、主体替换、场景复用、素材复用、新品套用老图。

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

External e-commerce sellers and creative teams use this skill to replace a product in an existing scene image with a new product reference while retaining the original scene, composition, and lighting.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: Images are uploaded to iqinghu/LinkPix for cloud processing, and the service retention practices were not verified.

Mitigation: Send only images you are authorized to share with the service.

Risk: The workflow uses service credentials and installs an external CLI dependency.

Mitigation: Protect the service token, prefer a reviewed CLI version, review upgrades, and check generation costs.

## Reference(s):

- [Clawhub skill release](https://clawhub.ai/autoagc/skills/linkpix-product-swap)
- [qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)

## Skill Output:

**Output Type(s):** [Generated images, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Generated images with Markdown guidance and inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Image output is a generative redraw rather than pixel-exact editing; review product details, text, logos, proportions, perspective, and reflections.]

## Skill Version(s):

0.1.8 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
