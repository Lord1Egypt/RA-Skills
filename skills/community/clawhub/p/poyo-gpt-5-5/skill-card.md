## Description:

GPT-5.5 chat completions on PoYo via the OpenAI-compatible `https://api.poyo.ai/v1/chat/completions` endpoint.

This skill is ready for commercial/non-commercial use.

## Publisher:

[coolhackboy](https://clawhub.ai/user/coolhackboy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to prepare PoYo GPT-5.5 chat-completion payloads, server-side curl requests, streaming options, and response parsing notes for text generation, coding help, reasoning, summarization, and workflow assistance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: PoYo API keys or private prompts could be exposed through client-side use, logs, screenshots, chat output, or process arguments on shared systems.

Mitigation: Keep `POYO_API_KEY` in server-side environment variables or a backend secret manager, avoid logging prompts or authorization headers, and harden shell invocation on shared machines.

Risk: The skill sends prompts to an external PoYo API endpoint.

Mitigation: Use it only when the user intends to use PoYo GPT-5.5 and trusts PoYo with the submitted data.

## Reference(s):

- [PoYo GPT-5.5 Model Page](https://poyo.ai/models/gpt-5-5)
- [PoYo Chat Completions API Docs](https://docs.poyo.ai/api-manual/chat-series/chat-completions)
- [Local API Reference](references/api.md)
- [ClawHub Skill Page](https://clawhub.ai/coolhackboy/skills/poyo-gpt-5-5)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON payload examples and bash curl commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses `POYO_API_KEY` and `curl` for optional server-side submissions; supports synchronous and streaming chat-completion guidance.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
