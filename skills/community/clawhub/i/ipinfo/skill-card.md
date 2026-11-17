## Description:

Perform IP geolocation lookups using ipinfo.io API. Convert IP addresses to geographic data including city, region, country, postal code, timezone, and coordinates. Use when geolocating IPs, enriching IP data, or analyzing geographic distribution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tiagom101](https://clawhub.ai/user/tiagom101)

### License/Terms of Use:


## Use Case:

Developers, analysts, and operations teams use this skill to enrich IP addresses with location, timezone, coordinate, and organization data from the IPinfo API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queried IP addresses, including the user's current public IP in the current-IP example, are sent to ipinfo.io.

Mitigation: Use the skill only when sharing those IP addresses with IPinfo is acceptable for the workflow and data policy.

Risk: An IPINFO_TOKEN can be exposed if pasted directly into commands, URLs, logs, or source files.

Mitigation: Store IPINFO_TOKEN in the OpenClaw dashboard or a protected environment variable, and rotate it if an authenticated URL is exposed.

## Reference(s):

- [IPinfo](https://ipinfo.io)
- [ClawHub IPinfo Skill](https://clawhub.ai/tiagom101/skills/ipinfo)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash and Python examples plus JSON response descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl for shell examples; optional IPINFO_TOKEN enables authenticated IPinfo requests.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
