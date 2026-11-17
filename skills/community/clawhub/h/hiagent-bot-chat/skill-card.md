## Description:

一个基于 hiagent 的智能助手技能，用于与 hiagent 进行对话。

This skill is ready for commercial/non-commercial use.

## Publisher:

[honglei24](https://clawhub.ai/user/honglei24)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to start or continue hiagent conversations, inspect conversation history, and send prompts through a configured hiagent API endpoint.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, user identifiers, conversation identifiers, and conversation metadata are sent to the configured hiagent API endpoint.

Mitigation: Use a trusted HTTPS HIAGENT_API_URL, confirm the service's retention and access controls, and avoid submitting sensitive prompts unless those controls are acceptable.

Risk: The skill requires an API key for hiagent API requests.

Mitigation: Use a least-privilege HIAGENT_API_KEY and manage it through environment variables or a secret store rather than hard-coding it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/honglei24/skills/hiagent-bot-chat)
- [Publisher profile](https://clawhub.ai/user/honglei24)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and the HIAGENT_API_URL, HIAGENT_API_KEY, and HIAGENT_USER_ID environment variables.]

## Skill Version(s):

0.0.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
