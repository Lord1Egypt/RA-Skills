## Description:

DingTalk (钉钉) integration - Send messages, create groups, and automate DingTalk workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lukaizj](https://clawhub.ai/user/lukaizj)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams use this skill to send DingTalk text or markdown messages, create group chats, list accessible chats, and automate DingTalk workflows from an agent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary flags a callable token tool that returns part of an access token.

Mitigation: Install only for trusted workflows, remove or disable the token tool before broad use, and avoid returning token substrings in tool results or logs.

Risk: The skill can send messages and create DingTalk chats through the configured app.

Mitigation: Scope DingTalk app permissions narrowly and require clear user confirmation before sending messages or creating chats.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lukaizj/skills/lukaizj-dingtalk)
- [Publisher profile](https://clawhub.ai/user/lukaizj)
- [Project homepage](https://github.com/lukaizj/dingtalk-integration-skill)
- [DingTalk Open Platform](https://open.dingtalk.com/)

## Skill Output:

**Output Type(s):** [Text, Markdown, API Calls, Shell commands, Configuration]

**Output Format:** [Markdown and structured tool-call results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires DingTalk App ID and App Secret environment variables; DingTalk Agent ID is optional in configuration.]

## Skill Version(s):

0.1.0 (source: release evidence and claw.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
