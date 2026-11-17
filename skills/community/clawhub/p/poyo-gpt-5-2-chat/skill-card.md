## Description:

GPT-5.2 chat completions on PoYo via the OpenAI-compatible chat completions API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[coolhackboy](https://clawhub.ai/user/coolhackboy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to prepare PoYo GPT-5.2 chat-completion payloads, curl examples, streaming guidance, and response parsing notes for server-side chat integrations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can help submit user-prepared chat payloads to a third-party PoYo API.

Mitigation: Use it only when PoYo API use is intended and approved; avoid sending private or regulated data unless policy allows it.

Risk: The PoYo API key is a secret required for execution.

Mitigation: Keep POYO_API_KEY server-side in an environment variable or secret manager, and do not expose it in browser code, logs, screenshots, repositories, or chat output.

Risk: Prepared payloads may contain sensitive user messages or unsupported optional parameters.

Mitigation: Review payload files before submission and verify current optional-parameter support in the PoYo documentation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/coolhackboy/skills/poyo-gpt-5-2-chat)
- [PoYo GPT-5.2 model page](https://poyo.ai/models/gpt-5-2)
- [PoYo chat completions API docs](https://docs.poyo.ai/api-manual/chat-series/chat-completions)
- [PoYo API key dashboard](https://poyo.ai/dashboard/api-key)
- [Local API reference](artifact/references/api.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown with JSON and bash examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include prepared chat payloads, curl commands, streaming notes, and server-side API key handling guidance.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
