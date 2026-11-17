## Description:

Helps agents prepare OpenAI-compatible DeepSeek V4 chat completion requests through PoYo, including model selection, payloads, curl examples, streaming notes, and response parsing guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[coolhackboy](https://clawhub.ai/user/coolhackboy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to select PoYo DeepSeek V4 Flash or Pro, prepare chat-completion payloads, and produce curl or integration guidance for synchronous and streaming workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The submit script sends the selected JSON chat payload to PoYo using POYO_API_KEY.

Mitigation: Review payloads for confidential content, keep POYO_API_KEY server-side, and make live calls only when intended.

Risk: API keys or private prompts could be exposed through browser code, logs, repositories, screenshots, or chat output.

Mitigation: Store keys in server-side environment variables or a secret manager and avoid logging private messages, system prompts, or authorization headers.

Risk: Streaming responses require an SSE-aware client.

Mitigation: Use streaming only when the integration can consume SSE; otherwise use synchronous chat completions.

## Reference(s):

- [PoYo DeepSeek V4 Chat API Reference](references/api.md)
- [PoYo Chat Completions API docs](https://docs.poyo.ai/api-manual/chat-series/chat-completions)
- [DeepSeek V4 Flash model page](https://poyo.ai/models/deepseek-v4-flash)
- [DeepSeek V4 Pro model page](https://poyo.ai/models/deepseek-v4-pro)
- [ClawHub skill page](https://clawhub.ai/coolhackboy/skills/poyo-deepseek-v4-chat)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON payloads and bash curl examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include synchronous or SSE streaming handling notes and server-side API-key handling guidance.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
