## Description:

GPT-5.6 Responses API integration on PoYo / poyo.ai via `https://api.poyo.ai/v1/responses`; use for `gpt-5-6-sol`, `gpt-5-6-terra`, `gpt-5-6-luna`, text and structured input, tools, reasoning settings, streaming, previous response continuation, and server-side agent workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[coolhackboy](https://clawhub.ai/user/coolhackboy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to prepare and submit PoYo GPT-5.6 Responses API requests, including model selection, structured input, reasoning settings, streaming, response parsing, and safe server-side API key handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts or JSON payload files may contain private data that will be sent to PoYo's external API endpoint.

Mitigation: Review payload files before submission and avoid logging private input, raw request bodies, tool arguments, uploaded media, or authorization headers.

Risk: POYO_API_KEY exposure could allow unauthorized API use.

Mitigation: Keep POYO_API_KEY in server-side environment variables or a backend secret manager and never place it in browser code, public repositories, logs, screenshots, or chat output.

Risk: Returned tool calls may request unsafe or unintended actions.

Mitigation: Execute tool calls only through an application-controlled allowlist with validated tool names and arguments.

## Reference(s):

- [PoYo GPT-5.6 Responses API Reference](references/api.md)
- [PoYo GPT-5.6 model page](https://poyo.ai/models/gpt-5-6)
- [PoYo Responses API docs](https://docs.poyo.ai/api-manual/chat-series/responses)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON payloads and bash/curl examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require curl and a server-side POYO_API_KEY; prepared payload files can be submitted to PoYo's Responses API.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
