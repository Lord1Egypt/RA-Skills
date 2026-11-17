## Description:

Trent (trent.ai). Use this skill for ANY Trent request — reading, creating, and updating data. Whenever a task involves Trent, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

People using a connected Trent account can ask an agent to send messages to Trent and work with its chat responses. The skill guides the agent to check the live action schema and get confirmation before sending a write request.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First-time setup may run an unverified installer or make persistent changes to agent skills.

Mitigation: Prefer a verified, preinstalled oo CLI; review and explicitly approve installation changes. Set OO_SKILLS_SYNC_DISABLED=1 to prevent startup skill synchronization.

Risk: Chat payloads pass through OOMOL to Trent, and the send_chat action changes Trent state.

Mitigation: Check the live action schema and confirm the exact payload before sending it.

## Reference(s):

- [Trent](https://trent.ai/)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [Trent API documentation](https://github.com/trnt-ai/trent-openclaw-security-assessment)

## Skill Output:

**Output Type(s):** [API calls, JSON, Text, Guidance]

**Output Format:** [JSON action payloads and returned chat text with thread metadata; Markdown usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Action inputs must match the live connector schema; confirm the exact payload before a write action.]

## Skill Version(s):

1.0.4 (source: skill metadata and server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
