## Description:

参考爆款商品图片，智能分析其设计风格并用你的商品生成相似视觉效果，快速打造高点击率主图。当用户要求照着某张爆款图做主图、对标竞品主图、复刻图片风格时必须触发。关键词：LinkPix、qhkit、主图复刻、爆款复刻、对标主图、竞品图风格、风格迁移、照着做、相似风格主图、高点击率主图。

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

面向电商运营者与商品卖家，依据一张参考主图和自有商品图生成风格相近的商品主图，并提示用户核对商品结构、文字与标识。

### Deployment Geography for Use:

China (the documented service setup targets the domestic iqinghu.com site)

## Known Risks and Mitigations:

Risk: Installing or upgrading the CLI may make software changes, and switching service sites can replace existing account settings.

Mitigation: Review setup before installation, use an isolated pinned CLI version, approve upgrades explicitly, and preserve current account configuration before switching sites.

Risk: Reference and product images are processed by an external image service, and generation can consume credits.

Mitigation: Submit only images authorized for external processing and check the applicable credit cost before generation.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/autoagc/skills/linkpix-main-image-clone)
- [qhkit package documentation](https://www.npmjs.com/package/@iqinghu/qhkit)

## Skill Output:

**Output Type(s):** [Images, Guidance, Shell commands]

**Output Format:** [Generated image outputs with concise text guidance and qhkit command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Image details can vary; users should check important product features, text, and logos in generated results.]

## Skill Version(s):

0.1.8 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
