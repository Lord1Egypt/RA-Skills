## Description:

用户指定 GPT Image 2.6 / 智慧模型2.6，要把商品图换成白底、清除背景、逐件处理一批商品或交付透明 PNG 时使用。

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

电商运营人员和商品内容创作者可用此技能将商品参考图处理为纯白背景素材，逐件处理商品批次，并在验证实际透明像素后交付透明 PNG。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected product images are uploaded to Qinghu for processing, and generation can incur charges.

Mitigation: Use the skill only when the user accepts the image transfer; show the requested inputs and estimated charge, then wait for approval before generation.

Risk: A configured QHKIT_BASE_HOST overrides QHKIT_ENV, and the external qhkit CLI is outside the reviewed artifact.

Mitigation: Check the configured service host before supplying credentials and review the CLI version and configuration before use.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/autoagc/skills/linkpix-gpt-image-2-6-white-background)

## Skill Output:

**Output Type(s):** [Images, Shell commands, Configuration, Guidance]

**Output Format:** [Image files and Markdown guidance with JSON examples and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Batch items are handled as separate generation tasks; transparent PNG delivery requires checking for actual alpha transparency.]

## Skill Version(s):

0.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
