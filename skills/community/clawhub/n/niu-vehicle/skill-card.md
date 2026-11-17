## Description:

Connects to NIU smart electric vehicles to retrieve real-time battery, charging, range, location, and mileage status.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qdsang](https://clawhub.ai/user/qdsang)

### License/Terms of Use:

MIT-0

## Use Case:

External NIU vehicle owners and agent users use this skill to check scooter battery level, charging status, remaining range or charge time, current location, and total mileage from NIU telemetry.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill needs access to a NIU API key and scooter telemetry, including current location.

Mitigation: Install only for agents and users that should access this telemetry, and store the API key in the configured secret source rather than in shared prompts or transcripts.

Risk: The API key is passed in a query URL, which can be exposed through shell tracing, shared process visibility, or logs.

Mitigation: Avoid shell tracing and shared logs when running the command, and rotate the NIU API key if the query URL may have been recorded.

Risk: Location responses can reveal sensitive vehicle or user whereabouts.

Mitigation: Share returned location data only with authorized users and avoid posting raw responses in public or persistent channels.

## Reference(s):

- [NIU homepage](https://www.niu.com/)
- [NIU scooter status API endpoint](https://ai-mcp.niu.com/claw/scooter_info?key=$NIU_API_KEY)
- [ClawHub skill page](https://clawhub.ai/qdsang/skills/niu-vehicle)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and NIU_API_KEY; queries NIU scooter telemetry including current location.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
