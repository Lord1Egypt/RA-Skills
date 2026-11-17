## Description:

Claude Fable 5 Messages API integration on PoYo / poyo.ai via `https://api.poyo.ai/v1/messages`; use when the user explicitly requests PoYo, `claude-fable-5`, or PoYo Messages API payloads involving content blocks, system prompts, tools, structured output, prompt caching controls, streaming, or server-side agent workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[coolhackboy](https://clawhub.ai/user/coolhackboy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to prepare and submit Claude Fable 5 Messages API payloads through PoYo, including system prompts, content blocks, tool definitions, structured output settings, streaming requests, and response parsing notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: PoYo API keys could be exposed if used in browser code, logs, screenshots, public repositories, or chat output.

Mitigation: Keep POYO_API_KEY in server-side environment variables or a backend secret manager and avoid logging API key headers.

Risk: Prepared messages, system prompts, tool definitions, image content, and other payload data are sent to PoYo when the script or curl examples are used.

Mitigation: Review each JSON payload before submission and install the skill only for workflows that intentionally use PoYo's Claude Fable 5 API.

Risk: Returned tool calls could trigger unintended actions if executed without application controls.

Mitigation: Execute returned tool calls only through an application-controlled allowlist with validated arguments.

## Reference(s):

- [PoYo Claude Fable 5 Messages API Reference](artifact/references/api.md)
- [PoYo Claude Fable 5 Model Page](https://poyo.ai/models/claude-fable-5)
- [PoYo Claude Messages API Documentation](https://docs.poyo.ai/api-manual/chat-series/claude-messages)
- [ClawHub Skill Page](https://clawhub.ai/coolhackboy/skills/poyo-claude-fable-5)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with JSON payload examples and bash curl commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include request payloads, streaming guidance, tool schema notes, and response parsing notes.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
