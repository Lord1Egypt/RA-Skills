## Description:

Gotify (gotify.net). Use this skill for ANY Gotify request — reading, creating, and updating data. Whenever a task involves Gotify, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Users with a connected Gotify account use the skill to check service health and version information or send Gotify messages. It checks each action's live schema before preparing a request, and requires confirmation before sending a message.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup instructions include remote installer commands, and the security review says setup permits remote code execution while broader agent changes are not fully disclosed.

Mitigation: Review and pin the CLI installation source, confirm which agent skills it will install or update, and disable startup skill synchronization with OO_SKILLS_SYNC_DISABLED when appropriate.

Risk: Sending a message changes Gotify state.

Mitigation: Confirm the exact message payload and effect with the user before running the send_message action.

## Reference(s):

- [Gotify](https://gotify.net)
- [Gotify push message documentation](https://gotify.net/docs/pushmsg)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [ClawHub skill page](https://clawhub.ai/oomol/skills/oo-gotify)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Shell commands, Guidance]

**Output Format:** [JSON action results with concise text guidance; shell commands for schema inspection and actions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Message sending changes Gotify state and requires confirmation of the exact payload and effect.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
