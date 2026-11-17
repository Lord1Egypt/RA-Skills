## Description:

生成迷你厨房烹饪短视频，支持从文字描述或公开 HTTPS 图片创建迷你厨具和食材的真实烹饪动效。

This skill is ready for commercial/non-commercial use.

## Publisher:

[zoucdr](https://clawhub.ai/user/zoucdr)

### License/Terms of Use:

MIT-0

## Use Case:

External creators and agent users use this skill to turn mini-kitchen cooking ideas or product-style images into short vertical video generation prompts and WeryAI generation requests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Custom WeryAI endpoint environment variables can redirect requests and expose prompts or API credentials to an untrusted service.

Mitigation: Use the official WeryAI endpoints unless a custom WERYAI_BASE_URL or WERYAI_MODELS_BASE_URL is fully trusted.

Risk: The WERYAI_API_KEY is required for generation and status operations, so misuse or leakage could affect the user's WeryAI account.

Mitigation: Keep the key scoped, rotate it regularly, and avoid sharing logs or environments that may expose it.

Risk: Interpolating JSON parameters into a shell command can create shell-environment risk.

Mitigation: Invoke Node with structured arguments and avoid shell string interpolation for user-provided JSON.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zoucdr/skills/mini-kitchen-video)
- [Publisher profile](https://clawhub.ai/user/zoucdr)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON CLI parameters and generated video URLs or API status JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses Node.js 18+ and WERYAI_API_KEY; supports text-to-video, image-to-video, multi-image generation, status polling, model listing, and dry-run request inspection.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
