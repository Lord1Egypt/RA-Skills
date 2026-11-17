## Description:

Huo15 DingTalk Connector Pro connects DingTalk messaging channels to OpenClaw agents with AI Card streaming, session management, rich media handling, and multi-agent routing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jobzhao15](https://clawhub.ai/user/jobzhao15)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to connect DingTalk enterprise chats to OpenClaw agents, route messages to one or more agents, and return streaming AI Card responses with session-aware context. It is intended for DingTalk/OpenClaw deployments that need chat-based access to agent actions, media handling, and document workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: DingTalk messages can grant broad authority to connected agents through the message-to-agent channel.

Mitigation: Configure direct-message and group allowlists or disable group access, and restrict which agents and tools the channel can reach.

Risk: Agent output may cause readable local files to be uploaded when file paths appear in responses.

Mitigation: Limit media upload behavior, restrict tool access, and run the connector only in environments where readable local files are appropriate to share.

Risk: The beta installer path is not independently verified by the server evidence.

Mitigation: Prefer the normal release installation flow and verify the exact commit before running any beta installer.

Risk: The security verdict is suspicious because the connector has broad messaging, attachment, and AI-response transmission capabilities.

Mitigation: Review the security guidance before deployment and treat the connector as able to transmit DingTalk messages, attachments, AI responses, and some local files readable by OpenClaw.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jobzhao15/skills/huo15-dingtalk-connector-pro)
- [ClawHub Publisher Profile](https://clawhub.ai/user/jobzhao15)
- [npm Package](https://www.npmjs.com/package/@huo15/dingtalk-connector-pro)
- [OpenClaw](https://openclaw.ai/)
- [DingTalk Open Platform](https://open-dev.dingtalk.com/)
- [Agent Routing and SessionKey Specification](artifact/docs/AGENT_ROUTING.md)
- [DingTalk DEAP Agent Integration](artifact/docs/DEAP_AGENT_GUIDE.en.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, API Calls, Configuration]

**Output Format:** [DingTalk messages, AI Card streaming responses, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can send or relay DingTalk text, rich media, document operations, and agent responses according to channel configuration.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
