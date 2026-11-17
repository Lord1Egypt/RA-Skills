## Description:

为真实商品规划并生成主图与轮播图套组；先核对商品、平台、卖点和素材，交付逐张画面清单、文案与验收标准，并在工具可用且用户确认费用后生成成片。

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

面向电商商家与商品运营人员，用商品参考图和已确认的卖点规划主图、轮播图或 SKU 图套组，并在条件满足时生成图片。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reference images are sent to iqinghu.com, and the external CLI implementation and service privacy practices are unverified.

Mitigation: Submit only reference images authorized for that service and check its retention terms before sending confidential material.

Risk: Image generation can incur a cost.

Mitigation: Review the estimate and confirm the cost before generation.

Risk: Installing or running an external CLI introduces dependency and privilege considerations.

Mitigation: Consider a reviewed, pinned CLI version and install without administrator privileges.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/autoagc/skills/linkpix-main-image-set)
- [qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)

## Skill Output:

**Output Type(s):** [Text, Markdown, Images, Image URLs]

**Output Format:** [Markdown plan with per-image tables and copy; generated image files or URLs when available]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Plans remain deliverable when image generation is unavailable; generated images are provided only after cost approval and successful generation.]

## Skill Version(s):

0.1.8 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
