## Description:

Zulip channel plugin for OpenClaw with topic threading, metadata DB, bot commands, and event queue processing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kagura-agent](https://clawhub.ai/user/kagura-agent)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw operators use this skill to connect an OpenClaw agent to a Zulip organization, route stream/topic and DM messages, and manage per-topic metadata through bot commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented sender controls appear unenforced while the plugin can forward chat messages and mutate stored metadata.

Mitigation: Review before installing and use only where everyone who can message the Zulip bot is allowed to invoke the agent and manage topic metadata.

Risk: Zulip API credentials could be exposed or misused if committed, sent to an untrusted realm, or scoped too broadly.

Mitigation: Require an HTTPS Zulip realm, avoid committing the API key, restrict the bot's stream access, and rotate credentials if exposed.

Risk: Dependency contents may not match an approved supply-chain source.

Mitigation: Update or regenerate the dependency lockfile from an approved registry before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kagura-agent/skills/openclaw-zulip)
- [Zulip REST API](https://zulip.com/api/rest)
- [Zulip](https://zulip.com)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Zulip messages, metadata command responses, and OpenClaw channel configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May send messages through Zulip and update topic metadata when the configured bot receives supported events or commands.]

## Skill Version(s):

0.1.0 (source: release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
