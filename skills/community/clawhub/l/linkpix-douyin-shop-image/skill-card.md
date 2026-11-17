## Description:

为抖音小店商家生成商品主图套图、详情长图和营销活动图，帮助适配短视频电商视觉素材。

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

抖音小店商家、短视频运营者和直播团队可用此技能生成商品主图套图、详情页长图、活动海报及相关短视频电商视觉素材。

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: An API key could be exposed if shared in chat during setup.

Mitigation: Configure the key locally through a protected environment or secret manager, and rotate any key already shared.

Risk: Uploaded product images are shared with Qinghu AI, and the supplied evidence does not verify image-retention practices.

Mitigation: Upload only images approved for sharing with Qinghu AI, and check the provider's retention practices before use.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/autoagc/skills/linkpix-douyin-shop-image)
- [qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)

## Skill Output:

**Output Type(s):** [Images, Guidance, Shell commands, Configuration instructions]

**Output Format:** [Generated product images with image URLs, plus Markdown guidance and inline shell command examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Image count, size, model, and style depend on the user's selected options.]

## Skill Version(s):

0.1.4 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
