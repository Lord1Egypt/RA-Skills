## Description: <br>
DeepSeek V4 chat on PoYo / poyo.ai via `https://api.poyo.ai/v1/chat/completions`; use for `deepseek-v4-flash`, `deepseek-v4-pro`, OpenAI-compatible chat payloads, system prompts, multi-turn messages, streaming chat, coding assistance, long-context analysis, and server-side chat integration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[coolhackboy](https://clawhub.ai/user/coolhackboy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to prepare PoYo DeepSeek V4 chat completion payloads, choose Flash or Pro model IDs, handle synchronous or streaming responses, and keep PoYo API keys server-side. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: PoYo API keys could be exposed if copied into browser code, logs, public repositories, screenshots, or chat output. <br>
Mitigation: Keep POYO_API_KEY in server-side environment variables or a backend secret manager and avoid logging authorization headers. <br>
Risk: Chat prompts and payloads may contain sensitive user, system, or business data sent to PoYo. <br>
Mitigation: Review payloads before using the helper script and send sensitive content only when PoYo is approved for that data. <br>
Risk: Streaming responses require clients that can correctly consume server-sent events. <br>
Mitigation: Use `stream: true` only with streaming-aware client handling; otherwise use synchronous chat completion requests. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/coolhackboy/skills/poyo-deepseek-v4-chat) <br>
- [PoYo chat completions documentation](https://docs.poyo.ai/api-manual/chat-series/chat-completions) <br>
- [DeepSeek V4 Flash model page](https://poyo.ai/models/deepseek-v4-flash) <br>
- [DeepSeek V4 Pro model page](https://poyo.ai/models/deepseek-v4-pro) <br>
- [Local API reference](references/api.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with JSON payload examples and bash curl commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include model selection, chat payloads, streaming notes, response parsing guidance, and server-side API key handling reminders.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
