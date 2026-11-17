## Description:

智能识别商品主体，一键替换图片背景，生成不同风格的营销场景图，无需 PS。当用户要求给商品图换背景、替换场景、白底图换成场景图、把商品放到某个场景里时必须触发。关键词：LinkPix、qhkit、换背景、更换背景、背景替换、场景替换、白底换场景、商品换背景、营销场景图、免PS。

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

External sellers and ecommerce teams use this skill to replace a product photo's background with a described marketing scene and create scene variations. Users should check generated images for changes to product text, logos, or structure.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic CLI upgrades and returned upgrade commands can change executable behavior.

Mitigation: Review upgrade commands before execution and prefer a reviewed, pinned qhkit version.

Risk: Selected images are uploaded to the service, and image generation consumes account credits.

Mitigation: Limit inputs to intended images, protect the service token, and review the estimated or actual credit cost before generating.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/autoagc/skills/linkpix-background-swap)
- [qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)

## Skill Output:

**Output Type(s):** [Images, Shell commands]

**Output Format:** [Generated image files returned as URLs, with Markdown guidance and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generative editing may change product details; review text, logos, and product structure in the results.]

## Skill Version(s):

0.1.8 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
