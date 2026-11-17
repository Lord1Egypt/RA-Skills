## Description:

聚合数据提供的 paid AI image generation skill that collects a prompt and size, calls Juhe's A2M HTTP 402 service, and hands payment completion to the Alipay payment skill.

This skill is ready for commercial/non-commercial use.

## Publisher:

[juhemcp](https://clawhub.ai/user/juhemcp)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to request paid AI image generation from text prompts through Juhe, with payment handled through Alipay before generation results are returned and saved locally.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompt text is sent to Juhe's paid third-party image service.

Mitigation: Tell users before collecting prompt parameters and avoid private, regulated, or sensitive information in prompts.

Risk: The security review flags unsafe install and shell-command patterns.

Mitigation: Verify the Alipay payment installer source and exact version before running it, and prefer a structured HTTP client over interpolated shell commands for API requests.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/juhemcp/skills/juhe-ai-image-generate-a2a)
- [Juhe A2A query endpoint](https://apis.juhe.cn/a2a/query)

## Skill Output:

**Output Type(s):** [Text, API Calls, Shell commands, Files, Guidance]

**Output Format:** [Markdown guidance with JSON request examples and shell command snippets; generated image files are downloaded locally.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prompt text is capped at 800 characters; image size maps to 1:1, 16:9, 4:3, 3:4, or 9:16.]

## Skill Version(s):

1.0.11 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
