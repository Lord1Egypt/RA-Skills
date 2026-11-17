## Description:

Helps agents prepare Claude 4.6 Messages API payloads, curl commands, streaming settings, tool-use requests, structured-output settings, and response parsing notes for PoYo.

This skill is ready for commercial/non-commercial use.

## Publisher:

[coolhackboy](https://clawhub.ai/user/coolhackboy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and integration engineers use this skill when building server-side workflows that call PoYo's Claude 4.6 Messages API. It is intended for preparing request payloads, shell commands, configuration notes, and response handling guidance after PoYo has been selected as the provider.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: PoYo API keys could be exposed if placed in client code, logs, public repositories, screenshots, or chat output.

Mitigation: Keep POYO_API_KEY in server-side environment variables or a backend secret manager, and avoid including raw key headers in examples or logs.

Risk: Prepared payloads may contain private user messages, system prompts, image content, or tool inputs that are sent to PoYo when the submit script is run.

Mitigation: Run the submit script only with user-chosen payloads that are approved for transmission to PoYo, and avoid logging sensitive request content.

Risk: Live API calls may be made before the user intends to send data to PoYo.

Mitigation: Make calls only after explicit user confirmation and from a trusted shell with a safe server-side environment.

## Reference(s):

- [Poyo Claude 4 6 Api on ClawHub](https://clawhub.ai/coolhackboy/skills/poyo-claude-4-6-api)
- [PoYo Claude 4.6 model page](https://poyo.ai/models/claude-4-6-api)
- [PoYo Claude Messages API documentation](https://docs.poyo.ai/api-manual/chat-series/claude-messages)
- [PoYo API key page](https://poyo.ai/dashboard/api-key)
- [PoYo Claude 4.6 Series Messages API Reference](artifact/references/api.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON payloads, curl examples, shell commands, and integration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include model identifiers, request parameters, streaming notes, tool definitions, structured-output settings, cache settings, and response parsing notes.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
