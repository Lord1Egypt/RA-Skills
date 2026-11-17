## Description:

Slack integration - Send messages, manage channels, and automate Slack workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lukaizj](https://clawhub.ai/user/lukaizj)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to connect an agent to Slack so it can send messages, list channels, and create public channels in an authorized workspace.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A Slack bot token may expose more workspace actions or channel access than the integration needs.

Mitigation: Install with a Slack bot token scoped only to the intended workspace and required permissions.

Risk: Message sending and channel creation are live Slack workspace actions.

Mitigation: Review the target channel, message text, and channel name before invoking write actions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/lukaizj/skills/lukaizj-slack)
- [Skill Homepage](https://github.com/lukaizj/slack-integration-skill)
- [Slack App Configuration](https://api.slack.com/apps)

## Skill Output:

**Output Type(s):** [API Calls, Configuration, JSON, Guidance]

**Output Format:** [JSON responses from Slack tool calls with setup guidance in Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SLACK_BOT_TOKEN with only the Slack scopes needed for the intended workspace actions.]

## Skill Version(s):

0.1.0 (source: release evidence and claw.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
