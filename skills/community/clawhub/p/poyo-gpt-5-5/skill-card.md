## Description: <br>
Helps agents prepare PoYo GPT-5.5 chat completion requests, including OpenAI-compatible message payloads, curl examples, streaming choices, and response parsing notes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[coolhackboy](https://clawhub.ai/user/coolhackboy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to prepare server-side PoYo GPT-5.5 chat-completion payloads, curl calls, streaming handling, and integration notes for text generation, coding help, reasoning, summarization, and structured assistant output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send prompts, code, or user messages to PoYo when used for GPT-5.5 chat completions. <br>
Mitigation: Review prompts and payloads before submission, avoid sending sensitive data unless policy allows it, and use the skill only when PoYo involvement is intended. <br>
Risk: The PoYo API key is required for live calls and could be exposed if copied into client code, logs, screenshots, public repositories, or chat output. <br>
Mitigation: Keep POYO_API_KEY in a server-side environment variable or secret manager and avoid logging authorization headers or raw request bodies. <br>
Risk: Streaming responses require an SSE-aware client and may be mishandled by simple synchronous parsers. <br>
Mitigation: Use streaming only when the caller can consume SSE; otherwise prepare a normal synchronous chat-completions request. <br>


## Reference(s): <br>
- [PoYo GPT-5.5 Chat Completions API Reference](references/api.md) <br>
- [PoYo chat completions documentation](https://docs.poyo.ai/api-manual/chat-series/chat-completions) <br>
- [PoYo GPT-5.5 model page](https://poyo.ai/models/gpt-5-5) <br>
- [PoYo API key dashboard](https://poyo.ai/dashboard/api-key) <br>
- [ClawHub skill page](https://clawhub.ai/coolhackboy/skills/poyo-gpt-5-5) <br>
- [Publisher profile](https://clawhub.ai/user/coolhackboy) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with JSON payload examples and inline bash commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include model id, chat payload, synchronous or streaming handling, system prompt constraints, and response parsing notes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
