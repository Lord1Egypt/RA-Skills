## Description:

This skill helps agents prepare PoYo Claude Opus 4.7 Messages API requests, including payloads, curl commands, streaming setup, tool-use configuration, structured output, and response parsing notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[coolhackboy](https://clawhub.ai/user/coolhackboy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill when they have chosen PoYo as the provider for Claude Opus 4.7 and need Claude-compatible Messages API payloads, server-side curl commands, or integration guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, messages, image content, tool inputs, and structured payloads may be sent to PoYo when a request is submitted.

Mitigation: Review payload JSON before submission and avoid sending private or policy-restricted content unless the deployment is approved for that data.

Risk: The PoYo API key can expose account access if placed in client code, logs, repositories, screenshots, or chat output.

Mitigation: Keep POYO_API_KEY in server-side environment variables or a backend secret manager and redact API headers from logs and shared outputs.

Risk: The helper script performs a live API request to the PoYo Claude Messages endpoint when run with a payload file.

Mitigation: Run it only from a trusted shell after confirming the payload should be sent to PoYo and that POYO_API_KEY is available in a safe server-side environment.

## Reference(s):

- [PoYo Claude Opus 4.7 model page](https://poyo.ai/models/claude-opus-4-7)
- [PoYo Claude Messages API docs](https://docs.poyo.ai/api-manual/chat-series/claude-messages)
- [PoYo Claude Opus 4.7 Messages API Reference](references/api.md)
- [ClawHub skill page](https://clawhub.ai/coolhackboy/skills/poyo-claude-opus-4-7)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON payloads and bash examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include PoYo request payloads, curl commands, streaming notes, and response parsing guidance.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
