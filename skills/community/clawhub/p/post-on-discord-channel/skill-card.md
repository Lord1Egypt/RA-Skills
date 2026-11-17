## Description:

Post On Discord Channel sends messages to Discord channels via webhooks with markdown, embeds, file attachments, and mention controls through AgentPMT-hosted remote tool calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentpmt](https://clawhub.ai/user/agentpmt)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation builders use this skill to post Discord notifications, reports, embeds, and attachments from agent workflows through an AgentPMT-hosted Discord webhook tool.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Discord webhook URLs and message or attachment contents are sent through AgentPMT and Discord.

Mitigation: Treat webhook URLs as secrets, keep inputs minimal, and avoid sending sensitive or regulated data.

Risk: The skill relies on mutable remote live instructions for schema and examples.

Mitigation: Review live instructions before production use and keep local safety rules authoritative.

Risk: Mention controls and text-to-speech can notify or disrupt broad Discord audiences.

Mitigation: Restrict allowed mentions, avoid broad pings unless intended, and leave text-to-speech disabled unless required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/agentpmt/skills/post-on-discord-channel)
- [AgentPMT marketplace page](https://www.agentpmt.com/marketplace/post-on-discord-channel)
- [Generated action schema](artifact/schema.md)

## Skill Output:

**Output Type(s):** [API Calls, Markdown, Files, Guidance]

**Output Format:** [JSON tool-call payloads and Discord markdown message content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can include rich embeds, mention controls, text-to-speech, and up to 10 base64-encoded file attachments per message.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
