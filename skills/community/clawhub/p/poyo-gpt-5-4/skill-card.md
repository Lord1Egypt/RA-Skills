## Description: <br>
GPT-5.4 chat completions on PoYo / poyo.ai via `https://api.poyo.ai/v1/chat/completions`; use for `gpt-5.4`, OpenAI-compatible chat payloads, coding help, reasoning, system prompts, multi-turn messages, streaming chat, max_tokens, and server-side chat integration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[coolhackboy](https://clawhub.ai/user/coolhackboy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to prepare PoYo GPT-5.4 chat completion payloads, curl requests, streaming guidance, and response parsing notes for text generation, coding help, reasoning, summarization, and structured assistant output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: PoYo API keys, private user messages, system prompts, raw request bodies, or authorization headers could be exposed if copied into browser code, public repositories, logs, screenshots, or chat output. <br>
Mitigation: Keep POYO_API_KEY server-side in an environment variable or secret manager, and avoid logging private prompts, request bodies, or authorization headers unless policy explicitly allows it. <br>
Risk: The helper script can send a prepared payload to PoYo, which may disclose prompt content to an external API if invoked for unrelated coding or summarization work. <br>
Mitigation: Use the skill only when PoYo GPT-5.4 chat completions are intended, review the payload before running the script, and make live calls only from a trusted server-side shell. <br>
Risk: Streaming responses require SSE-aware client handling. <br>
Mitigation: Set `stream: true` only when the client can consume server-sent events; otherwise use synchronous chat completions. <br>


## Reference(s): <br>
- [PoYo GPT-5.4 Chat Completions API Reference](references/api.md) <br>
- [PoYo Chat Completions Documentation](https://docs.poyo.ai/api-manual/chat-series/chat-completions) <br>
- [PoYo GPT-5.4 Model Page](https://poyo.ai/models/gpt-5-4) <br>
- [ClawHub Skill Page](https://clawhub.ai/coolhackboy/skills/poyo-gpt-5-4) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with JSON payload examples and bash curl commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include OpenAI-compatible chat payloads, curl commands, response parsing notes, streaming guidance, and server-side POYO_API_KEY handling.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
