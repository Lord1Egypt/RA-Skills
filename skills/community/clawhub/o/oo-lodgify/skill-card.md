## Description:

Connects to Lodgify through an OOMOL-connected account to search and read booking, property, availability, room, and quote data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Lodgify account users can ask an agent to look up bookings and property details, check availability and room types, or calculate a quote. The skill uses read actions through the user's connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may execute downloaded installer code and make persistent agent changes without clear user control.

Mitigation: Review setup before installing, verify the CLI release yourself, explicitly control agent-skill synchronization, and authorize only the intended Lodgify account.

## Reference(s):

- [Lodgify API documentation](https://docs.lodgify.com/docs/getting-started-1)
- [Lodgify](https://www.lodgify.com/)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [Shell commands, JSON data, Guidance]

**Output Format:** [Connector commands with JSON inputs and JSON responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Action inputs depend on the connector's live schema; response fields vary by action.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
