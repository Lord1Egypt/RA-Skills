## Description:

OpenAI (openai.com). Use this skill for ANY OpenAI request — reading, creating, updating, and deleting data. Whenever a task involves OpenAI, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use an OOMOL-connected OpenAI account to run OpenAI actions such as responses, model and batch queries, embeddings, audio, image generation, and moderation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup fallback directs the agent to run downloaded software that was not audited, without a separate approval step.

Mitigation: Review setup behavior, prefer a separately approved and verified CLI release, and require approval for local software or agent-configuration changes.

Risk: OOMOL intermediates the OpenAI connection and submitted data.

Mitigation: Review data handling before sending sensitive information through the connection.

Risk: OpenAI write and destructive actions can change or remove remote data.

Mitigation: Keep the documented confirmations for writes and destructive actions.

## Reference(s):

- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [OpenAI API reference](https://platform.openai.com/docs/api-reference)
- [OpenAI API](https://openai.com/api/)

## Skill Output:

**Output Type(s):** [Shell commands, API calls, JSON, Guidance]

**Output Format:** [Markdown instructions with oo CLI command examples and JSON payloads; action responses are JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions can read or change remote OpenAI data; write and destructive actions require user confirmation.]

## Skill Version(s):

1.0.6 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
