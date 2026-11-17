## Description:

MacOS Gemini image generation via OpenRouter for OpenClaw agents, with automated start notification, image generation, and media sending.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eardori](https://clawhub.ai/user/eardori)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to generate images from prompts through OpenRouter and send the resulting media in an automated agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts are sent to OpenRouter and generated media or captions may be sent through Telegram.

Mitigation: Avoid sensitive prompts and review token, prompt, media, and caption handling before installation.

Risk: The helper can fetch and save arbitrary URLs returned by a model.

Mitigation: Prefer a version that allowlists image provider URLs, blocks internal or private destinations, and verifies downloaded content type and size.

Risk: Server security evidence marks the release as suspicious and requiring review before installation.

Mitigation: Review the skill and scan findings before deployment, then install only if the external service and media-handling behavior fit the intended environment.

## Reference(s):

- [Hana Image Gen MacOS on ClawHub](https://clawhub.ai/eardori/skills/hana-image-gen-macos)
- [OpenRouter Chat Completions API endpoint](https://openrouter.ai/api/v1/chat/completions)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Files, Configuration instructions]

**Output Format:** [Markdown workflow steps with shell commands and JSON file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires OPENROUTER_API_KEY and TELEGRAM_BOT_TOKEN; helper writes generated image files and emits output paths as JSON.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
