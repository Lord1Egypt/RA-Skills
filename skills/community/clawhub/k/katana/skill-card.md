## Description:

Generate images, videos, and text/LLM completions via the imgnAI Katana API, with optional media post-processing workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[imgn](https://clawhub.ai/user/imgn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to route agent requests to Katana for image generation, video generation, LLM completions, model lookup, cost-aware request confirmation, polling, and ffmpeg-based media post-processing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses Katana API credentials and can initiate paid external requests.

Mitigation: Use a dedicated low-balance API key, keep the secrets file private, and require explicit review of model, prompt, and cost before submission.

Risk: Prompts, files, images, or videos may be sent to imgnAI's API, and local request tracking may persist request metadata.

Mitigation: Avoid sending sensitive data unless the selected privacy tier is appropriate, use trusted state and secrets paths, and disable prompt/result history from the Katana API page when needed.

Risk: The skill can propose local file changes for model catalogue updates and media post-processing outputs.

Mitigation: Review proposed llms.txt-driven updates before approval and inspect generated ffmpeg or file-writing commands before execution.

Risk: The skill instructs agents to avoid default subagent routing for Katana operations, which may conflict with repository isolation practices.

Mitigation: Use the skill only in workspaces where inline execution is acceptable, and be cautious in repositories that depend on AGENTS.md or subagent isolation rules.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/imgn/skills/katana)
- [imgnAI homepage](https://app.imgnai.com)
- [Katana API page](https://app.imgnai.com/katana-api)
- [Katana API reference](https://kat.imgnai.com/llms.txt)
- [Model catalogue](artifact/models.md)
- [Image workflow](artifact/workflows/image.md)
- [Video workflow](artifact/workflows/video.md)
- [Text workflow](artifact/workflows/text.md)
- [Post-processing workflow](artifact/workflows/post-process.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline JSON payloads and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce API request payloads, polling instructions, cost summaries, generated media URLs, text responses, and local ffmpeg commands.]

## Skill Version(s):

1.0.3 (source: frontmatter, release evidence, changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
