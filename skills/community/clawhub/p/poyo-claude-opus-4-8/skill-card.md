## Description:

Claude Opus 4.8 Messages API on PoYo / poyo.ai via `https://api.poyo.ai/v1/messages`; use for `claude-opus-4-8`, Claude-compatible messages, system prompts, multi-turn conversations, tools, structured output, prompt cache settings, vision content blocks, streaming, and server-side integration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[coolhackboy](https://clawhub.ai/user/coolhackboy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to prepare Claude Opus 4.8 Messages API payloads, curl commands, streaming calls, tool definitions, structured output settings, and server-side integration notes for PoYo.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys or private prompt data could be exposed if payloads, headers, logs, screenshots, or browser-side code include secrets or sensitive content.

Mitigation: Keep POYO_API_KEY in server-side environment variables or a backend secret manager, review payload JSON before submission, and avoid logging private prompts, user data, image content, tool inputs, or API key headers.

Risk: A prepared payload can send user-controlled content to PoYo when the submission script is run.

Mitigation: Use the submit script only from a trusted shell after explicitly reviewing the JSON payload and confirming that policy allows the included data to be sent to PoYo.

## Reference(s):

- [PoYo Claude Opus 4.8 Messages API Reference](references/api.md)
- [PoYo Claude Opus 4.8 model page](https://poyo.ai/models/claude-opus-4-8)
- [PoYo Claude Messages API docs](https://docs.poyo.ai/api-manual/chat-series/claude-messages)
- [ClawHub skill page](https://clawhub.ai/coolhackboy/skills/poyo-claude-opus-4-8)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with JSON payloads and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include synchronous or streaming handling, response parsing notes, and guidance for system prompts, tools, structured output, and cache settings.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
