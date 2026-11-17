## Description:

基于五层拆解法的AI图片提示词生成器，将模糊创意转化为结构化图像生成规格书，并适配 Midjourney、DALL-E 和 Stable Diffusion 输出。

This skill is ready for commercial/non-commercial use.

## Publisher:

[349840432m-dev](https://clawhub.ai/user/349840432m-dev)

### License/Terms of Use:

MIT-0

## Use Case:

Creators, designers, and developers use this skill to turn rough image ideas into structured prompt specifications and ready-to-use prompts for Midjourney, DALL-E, Stable Diffusion, and general Chinese image-generation tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-entered creative briefs are sent through the local OpenClaw Gateway to the configured model provider.

Mitigation: Confirm that the configured provider is trusted and avoid entering confidential creative briefs or client material unless that provider is approved.

Risk: The skill depends on Gateway routing and the configured model provider for generated prompt quality and data handling.

Mitigation: Review the generated prompt before reuse and verify the Gateway configuration before installation or deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/349840432m-dev/skills/image-prompt-generator)
- [README](artifact/README.md)
- [Skill definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown prompt specification with Chinese sections and optional English tool-specific prompt blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes tool-specific variants for Midjourney, DALL-E, Stable Diffusion, and a general Chinese prompt.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter and claw.json list 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
