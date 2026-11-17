## Description:

Claude 4.5 Series Messages API on PoYo / poyo.ai via https://api.poyo.ai/v1/messages; helps agents prepare Claude-compatible request payloads, curl calls, streaming setup, tool-use configuration, structured output settings, and response parsing notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[coolhackboy](https://clawhub.ai/user/coolhackboy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill when preparing server-side PoYo Claude 4.5 Messages API integrations, including request payloads, curl commands, streaming handling, tool-use payloads, structured output settings, and response parsing notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional curl script can expose POYO_API_KEY to local process inspection while a request runs.

Mitigation: Keep POYO_API_KEY server-side and prefer a safer client or header/config-file approach when local process monitoring is a concern.

Risk: Request payloads, prompts, image content, tool inputs, and messages are transmitted to PoYo when a live API call is made.

Mitigation: Review payload JSON before sending, avoid logging private content or raw API key headers, and make live calls only from a trusted server-side environment.

## Reference(s):

- [PoYo Claude 4.5 model page](https://poyo.ai/models/claude-4-5-api)
- [PoYo Claude Messages API docs](https://docs.poyo.ai/api-manual/chat-series/claude-messages)
- [Local PoYo API reference](references/api.md)
- [ClawHub skill page](https://clawhub.ai/coolhackboy/skills/poyo-claude-4-5-api)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON payload examples, shell commands, configuration notes, and response parsing guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should include the selected model id, payload or parameter summary, synchronous or streaming handling, and security notes when credentials or private payload data are involved.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
