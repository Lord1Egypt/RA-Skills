## Description:

mcp-storyboard helps agents generate storyboard, story-scene, and picture-book images with BizyAir API support for prompt enhancement, aspect ratios, and batch generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bozoyan](https://clawhub.ai/user/bozoyan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content creators use this skill to generate storyboard panels, illustrated story scenes, and picture-book images from text prompts. It supports batch image generation, common aspect ratios, and long-running BizyAir task polling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and generation parameters are sent to BizyAir using the user's API key.

Mitigation: Use only with prompts that are appropriate to share with BizyAir, and avoid proprietary, private, or sensitive story material unless that data sharing is approved.

Risk: Automatic prompt rewriting can add sexualized adult-woman and demographic-specific descriptors to ordinary person or character prompts.

Mitigation: Review or remove the automatic model prompt suffix before deployment, use the opt-out control when available, and avoid use for minors, children, sensitive stories, or ordinary character prompts without explicit review.

Risk: Generated images may be unsuitable or inconsistent with the intended story context.

Mitigation: Review generated images and URLs before publication or reuse, especially for external-facing, brand, educational, or audience-sensitive material.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/bozoyan/skills/mcp-storyboard)
- [BizyAir MCP Endpoint](https://api.bizyair.cn/w/v1/mcp/242)
- [BizyAir Webapp Task API Endpoint](https://api.bizyair.cn/w/v1/webapp/task/openapi)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown text with generated image URLs and status or error guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include image preview links, generated image URLs, dimensions, batch size, and progress updates for long-running tasks.]

## Skill Version(s):

1.0.0 (source: server release evidence, released 2026-03-18)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
