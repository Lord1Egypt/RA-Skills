## Description:

Helps Hermes check Portveil VPN protection and move, rotate, reconnect, or add devices using US and Finland exits.

This skill is ready for commercial/non-commercial use.

## Publisher:

[roybogs](https://clawhub.ai/user/roybogs)

### License/Terms of Use:

MIT-0

## Use Case:

Portveil account holders and their agents use this skill to check device protection and manage VPN exit locations, reconnections, rotations, and device setup on request.

### Deployment Geography for Use:

Global; documented VPN exits are in the United States and Finland.

## Known Risks and Mitigations:

Risk: A token with control or admin scope can change VPN connectivity or add devices.

Mitigation: Use a dedicated token with read scope by default; grant control or admin only when needed and revoke it if the machine is no longer trusted.

Risk: Moving or disconnecting a device changes its network connection.

Mitigation: Make network changes only at the account owner's request and confirm disruptive or permanent actions before proceeding.

## Reference(s):

- [Portveil skill on ClawHub](https://clawhub.ai/roybogs/skills/portveil)
- [Publisher profile](https://clawhub.ai/user/roybogs)
- [Portveil](https://portveil.com)
- [Portveil dashboard](https://portveil.com/dashboard/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance]

**Output Format:** [Conversational text with setup commands when needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports device protection and exit location; setup guidance may include commands for a new device.]

## Skill Version(s):

1.0.3 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
