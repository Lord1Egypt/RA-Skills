## Description:

上架前平台合规校验与自动修复。待上架图 → Amazon / TikTok Shop / Temu / Shopee / 淘宝 各平台的通过或驳回风险报告，可一键修成合规图。当用户说「会不会被驳回」「合规检查」「白底不达标」「主图规格」「传上去被拒」时使用。

This skill is ready for commercial/non-commercial use.

## Publisher:

[dlazyai](https://clawhub.ai/user/dlazyai)

### License/Terms of Use:

MIT-0

## Use Case:

E-commerce sellers and operators use the skill to check product listing images against marketplace image rules, review rejection risks, and apply supported geometry or color fixes before upload.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A confirmed image-validation exit-status issue could let unreadable images pass a CI validation gate.

Mitigation: Consider avoiding installation until the issue is addressed; if used before then, verify unreadable-image handling and do not rely on the gate's exit status alone.

Risk: The security scan assessed only 60% of components fully, with four components assessed partially; use also involves external image services and network or environment access.

Mitigation: Treat the scan as incomplete and confirm that the external image services and required network or environment access match your expectations before use.

## Reference(s):

- [Platform image specifications](references/platform-specs.md)
- [detect-task visual checks](https://github.com/dlazy-ai/ecommerce-skills/blob/main/skills/detect-task/skill.md)
- [remove-watermark skill](https://github.com/dlazy-ai/ecommerce-skills/blob/main/skills/remove-watermark/skill.md)
- [item-repair skill](https://github.com/dlazy-ai/ecommerce-skills/blob/main/skills/item-repair/skill.md)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Image files]

**Output Format:** [Human-readable or JSON compliance report; processed image files when --fix is used]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports cover a machine-checkable subset of platform rules; text, watermark, and collage checks require visual review.]

## Skill Version(s):

1.0.32 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
