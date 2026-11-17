## Description:

一键提取图片中的印花图案，生成高清、平铺、可复用的图案素材，适用于 POD 定制及服装设计。当用户要求提取印花、抠图案、把衣服上的图案拿出来、图案素材化时必须触发。关键词：LinkPix、qhkit、印花提取、图案提取、提取花纹、POD素材、图案素材、印花设计稿、pattern。

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

External users and apparel/POD designers use the skill to turn a clothing or product image into a reusable, flat pattern design image.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: Source images are uploaded to LinkPix and image generation may use account credits.

Mitigation: Upload only images you are comfortable sending to the service and expect account-credit charges.

Risk: The CLI setup or upgrade can affect existing qhkit settings, and the API token grants account access.

Mitigation: Check existing settings before setup or upgrade and protect the API token.

Risk: Generative redraw can change small pattern details, and recognizable brand or IP artwork can carry rights concerns.

Mitigation: Review key design elements in the result and confirm you have rights to use branded artwork.

## Reference(s):

- [qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)
- [LinkPix POD materials workspace](https://www.iqinghu.com)
- [ClawHub skill release](https://clawhub.ai/autoagc/skills/linkpix-pod-pattern-extract)

## Skill Output:

**Output Type(s):** [Image files, Guidance, Shell commands]

**Output Format:** [Generated white-background raster pattern design with concise usage guidance and qhkit commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated details may differ slightly from the source; output is a bitmap, not vector artwork or a transparent layer.]

## Skill Version(s):

0.1.8 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
