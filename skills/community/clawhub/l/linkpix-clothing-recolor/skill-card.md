## Description:

一键生成服装的不同颜色版本，尽量保持版型、材质和光影一致，帮助制作 SKU 色卡图。

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

External users and ecommerce teams use the skill to create alternate clothing color images and SKU color cards from an existing product photo. It provides prompts and qhkit commands for recoloring while preserving garment details as much as possible.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Product images are uploaded to a generation service.

Mitigation: Upload only images you are authorized to use.

Risk: The CLI uses a service token and image generation may incur costs.

Mitigation: Protect the token and check generation costs before submitting jobs.

Risk: Installing or upgrading the CLI runs external software.

Mitigation: Prefer a reviewed, pinned CLI version, install without administrator privileges, and review upgrades before execution.

## Reference(s):

- [qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)
- [LinkPix Clothing Recolor on ClawHub](https://clawhub.ai/autoagc/skills/linkpix-clothing-recolor)

## Skill Output:

**Output Type(s):** [Images, Shell commands, Guidance]

**Output Format:** [Generated clothing recolor images with qhkit shell commands and usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated garment details may vary; review text, logos, and product structure in the resulting images.]

## Skill Version(s):

0.1.8 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
