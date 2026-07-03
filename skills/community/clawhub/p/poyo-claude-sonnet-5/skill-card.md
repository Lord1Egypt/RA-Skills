## Description: <br>
Claude Sonnet 5 chat on PoYo / poyo.ai via `https://api.poyo.ai/v1/messages`; use for `claude-sonnet-5`, Claude-compatible messages, coding agents, long-context chat, system prompts, tool use, structured output, prompt cache settings, vision content blocks, streaming, and server-side integration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[coolhackboy](https://clawhub.ai/user/coolhackboy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and coding agents use this skill to prepare Claude-compatible PoYo Messages API payloads, curl calls, streaming requests, tool definitions, structured output settings, and response parsing notes for Claude Sonnet 5. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, messages, tool inputs, and other payload data are sent to PoYo when the skill is used for live API calls. <br>
Mitigation: Use the skill only when PoYo is trusted for the data being sent, and avoid sending sensitive content unless product policy allows it. <br>
Risk: The included submit script makes a live API call with the provided JSON payload. <br>
Mitigation: Review the payload first and run the script only from a trusted server-side shell with `POYO_API_KEY` stored as an environment secret. <br>
Risk: API keys can be exposed if placed in browser code, logs, public repositories, screenshots, or chat output. <br>
Mitigation: Keep `POYO_API_KEY` server-side in environment variables or a backend secret manager and avoid logging request headers or secrets. <br>


## Reference(s): <br>
- [PoYo Claude Messages API documentation](https://docs.poyo.ai/api-manual/chat-series/claude-messages) <br>
- [PoYo Claude Sonnet 5 model page](https://poyo.ai/models/claude-sonnet-5) <br>
- [API reference](references/api.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with JSON payloads and bash examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include synchronous or streaming handling notes, tool-use configuration, structured output settings, cache settings, and response parsing guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
