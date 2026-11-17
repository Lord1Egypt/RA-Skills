## Description:

使用 LinkPix 的 qhkit 命令为电商商品图、营销图和海报生成图片 5.0 Flash 图像，支持文字提示和参考图。

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

External sellers and marketing teams use the skill to create product images, promotional visuals, and posters from text prompts or reference images. It provides guidance for selecting image options, estimating cost, and preparing generation requests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill's setup instructions ask users to share an API key in chat.

Mitigation: Configure credentials locally outside chat; replace any key already shared.

Risk: Reference images are uploaded to iqinghu.com during generation preparation, including prompt polishing.

Mitigation: Use only reference images that are appropriate to send to iqinghu.com, including during prompt polishing.

Risk: The external CLI implementation and the service's image-retention practices were not verified.

Mitigation: Review dependency installations and upgrades, and avoid sending images whose contents or retention would be unacceptable.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/autoagc/skills/linkpix-seedream-5-lite)
- [qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)

## Skill Output:

**Output Type(s):** [Images, Text, Shell commands, Configuration instructions]

**Output Format:** [Generated image URLs with concise Markdown guidance and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generation requests require user confirmation of parameters and estimated credit cost before submission.]

## Skill Version(s):

0.1.4 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
