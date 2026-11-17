## Description:

Control and query HomeKit and Home Assistant smart home devices via the Itsyhome macOS app.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nickustinov](https://clawhub.ai/user/nickustinov)

### License/Terms of Use:


## Use Case:

External users and smart-home operators use this skill to ask an agent to inspect device state, list rooms or devices, and control HomeKit or Home Assistant devices through the local Itsyhome app.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can trigger physical or security-sensitive actions such as unlocking doors, opening garages, or running scenes.

Mitigation: Require explicit user confirmation before any lock, garage, door, or physical/security-impact scene action.

Risk: The local Itsyhome webhook can control smart-home devices if exposed to an untrusted gateway or network.

Mitigation: Use the skill only where the OpenClaw gateway is trusted and the Itsyhome webhook is restricted to local access.

Risk: Device or room names could be unsafe if inserted directly into shell commands.

Mitigation: URL-encode device and room targets and avoid interpolating user-provided names into shell commands without validation.

## Reference(s):

- [Itsyhome app](https://itsyhome.app)
- [Itsyhome Webhook API Reference](references/api.md)
- [ClawHub Skill Page](https://clawhub.ai/nickustinov/skills/itsyhome-control)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and JSON response descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include local HTTP curl commands, URL-scheme commands, exact device targets, and concise user confirmations.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
