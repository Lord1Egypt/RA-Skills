## Description:

Deploys a four-agent chat and collaboration hub with chat server, moderator, translator, and archive-bot roles.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teoslayer](https://clawhub.ai/user/teoslayer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to set up a self-hosted multi-agent chat hub with moderation, translation, presence, threaded conversations, archival, and backups.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Chat messages may be moderated, translated, archived, indexed, backed up, and routed across multiple agents.

Mitigation: Use the skill only where operators and participants understand those data flows, and restrict translation or archival for private or sensitive rooms.

Risk: Trust relationships, retention behavior, and dependency controls are under-specified for a multi-agent chat deployment.

Mitigation: Pin and verify installed pilot-* skills, manually confirm trust handshakes, and define archive retention and deletion rules before use.

## Reference(s):

- [Pilot Protocol](https://pilotprotocol.network)
- [ClawHub Skill Page](https://clawhub.ai/teoslayer/skills/pilot-chat-collaboration-hub-setup)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with Bash and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes role-specific setup steps, trust handshakes, hostnames, data-flow descriptions, and manifest templates.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
