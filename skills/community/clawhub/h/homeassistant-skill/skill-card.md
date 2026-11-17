## Description:

Helps agents inspect, troubleshoot, and operate an existing Home Assistant installation through REST and supported WebSocket workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anotb](https://clawhub.ai/user/anotb)

### License/Terms of Use:

MIT

## Use Case:

People and developers with an existing Home Assistant installation use this skill to discover devices and capabilities, diagnose issues, and perform specifically authorized home actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A Home Assistant token can expose household information and authorize device actions.

Mitigation: Use a dedicated least-privilege account where possible, keep the token in a private environment or secret store, and prefer verified HTTPS.

Risk: Device actions, scenes, scripts, and automations can cause physical or security-sensitive changes.

Mitigation: Inspect targets and indirect effects, and get explicit confirmation before locks, alarms, garage doors, security automations, and broad batches.

Risk: Presence, location, calendar, and history results can reveal household routines; notifications and speech can disclose information to others.

Mitigation: Read only the needed data, keep results private, and confirm recipients, devices, and message content before notification or speech actions.

## Reference(s):

- [Project homepage (listed in skill metadata)](https://github.com/anotb/homeassistant-skill)
- [Modern Home Assistant workflows](references/modern-workflows.md)
- [REST examples](references/rest-examples.md)
- [Home Assistant REST API documentation](https://developers.home-assistant.io/docs/api/rest/)
- [Home Assistant WebSocket API documentation](https://developers.home-assistant.io/docs/api/websocket/)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown with shell examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only queries can return Home Assistant data; device actions require user authorization.]

## Skill Version(s):

2.2.0 (source: skill metadata, CHANGELOG)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
