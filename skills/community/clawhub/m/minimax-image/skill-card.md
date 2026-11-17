## Description:

使用MiniMax图像生成API进行文生图，支持文字描述生成图片，适用于PPT配图、封面图、内容配图等场景。

This skill is ready for commercial/non-commercial use.

## Publisher:

[taoj2025](https://clawhub.ai/user/taoj2025)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content creators use this skill to call the MiniMax text-to-image API from an agent workflow, generate image URLs from prompts, and optionally save returned images locally.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts are sent to the MiniMax API and may contain sensitive or proprietary text.

Mitigation: Use only prompts that are approved for third-party API processing and avoid confidential, regulated, or customer-sensitive content unless appropriate agreements and controls are in place.

Risk: The skill automatically downloads image URLs returned by the remote API without validating URL destination, content type, or response size.

Mitigation: Run with limited filesystem and network access; add URL allowlisting, response size limits, and content-type checks before routine or sensitive-environment use.

Risk: The MiniMax API key is required for operation and could be exposed through environment or command execution practices.

Mitigation: Store MINIMAX_API_KEY in a managed secret store or restricted environment variable and avoid printing, committing, or sharing the key.

Risk: The skill depends on the requests package without pinned dependency versions.

Mitigation: Pin dependencies and scan the runtime environment before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/taoj2025/skills/minimax-image)
- [Publisher profile](https://clawhub.ai/user/taoj2025)
- [MiniMax platform](https://platform.minimaxi.com/)
- [MiniMax image generation API endpoint](https://api.minimaxi.com/v1/image_generation)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell examples; runtime output is JSON-like image URL data and saved image files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a MiniMax API key via MINIMAX_API_KEY or explicit client configuration; generation count is clamped to 1-4 images.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
