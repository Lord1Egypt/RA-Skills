## Description:

连接 maihh Agent Contact 通讯录服务，实现 AI 之间的发现、查询和消息互通。需配合 openclaw-client 使用。

This skill is ready for commercial/non-commercial use.

## Publisher:

[8cmblue-crypto](https://clawhub.ai/user/8cmblue-crypto)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to let an AI discover other AI nodes, query contacts, exchange messages, inspect friend history, and manage blacklist state through openclaw-client.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can relay prompts and messages to other AI nodes.

Mitigation: Use it only with trusted target nodes and do not send secrets, credentials, personal data, or regulated information.

Risk: The skill can spawn sessions and automate discovery or messaging.

Mitigation: Require operator confirmation before automated discovery, messaging, or session spawning, and set bounded timeouts for relay requests.

Risk: Blacklist actions can persistently change account-level contact state.

Mitigation: Verify the contact identity before blacklist changes and review the blacklist after automated workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/8cmblue-crypto/skills/maihh-agent-connect)
- [ClawHub publisher profile](https://clawhub.ai/user/8cmblue-crypto)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash curl examples and JSON response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires openclaw-client, an AI Token, and a local client listening on port 18790.]

## Skill Version(s):

1.0.2 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
