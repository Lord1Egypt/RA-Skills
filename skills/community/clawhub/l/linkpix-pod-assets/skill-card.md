## Description:

面向 POD（Print on Demand）卖家生成设计素材：印花提取、印花贴合（mockup 效果图）、印花裂变、商品效果图，覆盖服饰、家居、饰品等 POD 品类的设计与上架。

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

POD 卖家可用此技能从参考图提取印花、生成图案变体，并制作服饰及其他商品的 mockup 效果图，用于设计和商品上架。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic installation or upgrades can make unreviewed changes to the user's environment.

Mitigation: Constrain dependency changes to a reviewed package version and require approval for upgrades; preserve existing CLI configuration.

Risk: Artwork uploads and image generation can involve user content and paid credits.

Mitigation: Confirm which artwork may be uploaded to iqinghu.com and set a credit budget before generation. Do not automatically execute commands supplied in CLI messages.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/autoagc/skills/linkpix-pod-assets)
- [qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)
- [LinkPix POD素材工作台](https://www.iqinghu.com)

## Skill Output:

**Output Type(s):** [Images, Text, Markdown, Shell commands, Configuration guidance]

**Output Format:** [Generated image assets with Markdown guidance and inline JSON/bash CLI examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated print details may vary; review key artwork elements before use.]

## Skill Version(s):

0.1.8 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
