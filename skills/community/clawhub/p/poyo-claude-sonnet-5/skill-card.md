## Description:

Claude Sonnet 5 chat on PoYo / poyo.ai via `https://api.poyo.ai/v1/messages`; use for `claude-sonnet-5`, Claude-compatible messages, coding agents, long-context chat, system prompts, tool use, structured output, prompt cache settings, vision content blocks, streaming, and server-side integration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[coolhackboy](https://clawhub.ai/user/coolhackboy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and coding agents use this skill to prepare Claude-compatible Messages API payloads, curl calls, tool-use settings, structured output settings, streaming requests, and response parsing notes for PoYo's Claude Sonnet 5 endpoint.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: PoYo API keys or private prompt content could be exposed if payloads, logs, screenshots, browser code, or public repositories include secrets or sensitive data.

Mitigation: Keep POYO_API_KEY in server-side environment variables or a secret manager, review payloads before submission, and avoid logging API keys, private messages, image content, tool inputs, or raw authorization headers.

Risk: Prepared payloads may send private prompts, images, or tool inputs to PoYo when a live API call is made.

Mitigation: Submit payloads only from a trusted shell after confirming the data is acceptable for the user's PoYo account and data policy.

Risk: Streaming requests require clients that can correctly consume streaming responses.

Mitigation: Use `stream: true` only when the calling client implements streaming-aware handling.

## Reference(s):

- [PoYo Claude Sonnet 5 model page](https://poyo.ai/models/claude-sonnet-5)
- [PoYo Claude Messages API docs](https://docs.poyo.ai/api-manual/chat-series/claude-messages)
- [PoYo API key page](https://poyo.ai/dashboard/api-key)
- [Skill API reference](references/api.md)
- [ClawHub skill page](https://clawhub.ai/coolhackboy/skills/poyo-claude-sonnet-5)
- [Publisher profile](https://clawhub.ai/user/coolhackboy)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with JSON payloads and bash/curl examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include prepared Claude Messages API payloads, streaming notes, tool definitions, structured output settings, and response parsing guidance.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
