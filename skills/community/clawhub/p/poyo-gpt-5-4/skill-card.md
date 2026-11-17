## Description:

GPT-5.4 chat completions on PoYo via OpenAI-compatible chat payloads, including examples for synchronous and streaming requests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[coolhackboy](https://clawhub.ai/user/coolhackboy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to prepare PoYo gpt-5.4 chat completion payloads, curl calls, and integration guidance while keeping API keys server-side.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys could be exposed if POYO_API_KEY or authorization headers are copied into browser code, logs, screenshots, repositories, or chat output.

Mitigation: Keep POYO_API_KEY in server-side environment variables or a backend secret manager and avoid logging raw authorization headers.

Risk: Prompts, system messages, and submitted payload content are sent to PoYo's API when the helper script is invoked.

Mitigation: Submit only payloads intended for PoYo and avoid logging private user messages, system prompts, or raw request bodies unless policy allows it.

Risk: The shell helper can make a live API request if invoked with a prepared payload and a configured POYO_API_KEY.

Mitigation: Run the script only from a trusted shell when the user explicitly asks to submit a prepared JSON payload.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/coolhackboy/skills/poyo-gpt-5-4)
- [PoYo GPT-5.4 model page](https://poyo.ai/models/gpt-5-4)
- [PoYo chat completions API docs](https://docs.poyo.ai/api-manual/chat-series/chat-completions)
- [API reference](references/api.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON and bash snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses POYO_API_KEY for optional server-side curl submission; no live API call unless explicitly requested.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
