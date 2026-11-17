## Description:

Build a chat, reasoning, or tool-calling agent on top of Runware-hosted LLMs using an OpenAI-compatible chat-completions and tool-calling loop.

This skill is ready for commercial/non-commercial use.

## Publisher:

[runware](https://clawhub.ai/user/runware)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to build conversational, reasoning, or tool-calling agents over their own functions using Runware-hosted LLMs and the OpenAI-compatible chat-completions format.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, message history, tool schemas, and tool results may be processed by Runware's hosted API.

Mitigation: Use this skill only when third-party API processing is acceptable, avoid sensitive data unless approved, and configure the Runware API key according to local credential-handling policy.

Risk: Exposed tools can let an agent act on systems through user-defined functions.

Mitigation: Keep tools narrowly scoped, validate tool arguments, return compact structured results, and bound the tool-call loop with an iteration cap.

## Reference(s):

- [LLM agent worked recipes](references/examples.md)
- [Runware OpenAI-compatible API endpoint](https://api.runware.ai/v1)
- [ClawHub skill page](https://clawhub.ai/runware/skills/llm-agent)
- [runware publisher profile](https://clawhub.ai/user/runware)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, configuration, shell commands]

**Output Format:** [Markdown with JSON and code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include OpenAI-compatible chat-completions payloads, tool schemas, tool-call loop guidance, and integration checks for Runware-hosted LLMs.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
