## Description:

An AI receptionist for an existing phone number that screens calls, takes messages and booking requests, and lets users manage call handling through OsmO.

This skill is ready for commercial/non-commercial use.

## Publisher:

[getosmo](https://clawhub.ai/user/getosmo)

### License/Terms of Use:

MIT-0

## Use Case:

External users and businesses use the skill to handle inbound calls on an existing phone number, review call summaries and recordings, manage caller rules, and check bookings through their OsmO account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Using OsmO requires connecting to its hosted service and enabling call forwarding, which routes inbound calls through the receptionist.

Mitigation: Review OsmO's privacy information and enable forwarding only when comfortable with the service handling those calls.

Risk: The security scan was incomplete, and permissions were not fully assessed.

Mitigation: Review the available tools and requested permissions before connecting the service.

## Reference(s):

- [OsmO](https://getosmo.app)
- [OsmO MCP service](https://api.getosmo.app/mcp)

## Skill Output:

**Output Type(s):** [Text, API Calls, Configuration, Guidance]

**Output Format:** [Text summaries and structured call, booking, and account information; service settings can be updated through OsmO.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Accesses the signed-in account's call and receptionist data; service changes are made only after user approval.]

## Skill Version(s):

1.1.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
