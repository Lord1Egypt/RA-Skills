## Description:

Looks up geographic and ASN information for public IPv4 and IPv6 addresses, including IPs resolved from domains, through a fixed MCP geolocation service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[marc-chen](https://clawhub.ai/user/marc-chen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and external users can use this skill to answer IP or domain geolocation questions, compare batches of public IPs, and return concise country, city, and ASN details. It is suited for quick network investigation and support workflows where public IP metadata is useful.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Public IP addresses and IPs resolved from domains are sent to ip.api4claw.com over HTTPS.

Mitigation: Use the skill only when that external lookup is acceptable; avoid sensitive internal network data and prefer a self-hosted or first-party geolocation source for privacy-sensitive workflows.

Risk: Private or reserved addresses could expose internal network context if queried externally.

Mitigation: The helper script blocks common private and reserved IPv4 and IPv6 ranges before external lookup, and users should review inputs before calling the MCP service directly.

Risk: Geolocation and country text can be incomplete, empty, or affected by client encoding issues.

Mitigation: Keep raw values visible, include country_code for reliability, use '-' for empty fields, and do not fabricate missing location details.

## Reference(s):

- [MCP API Reference](artifact/references/api.md)
- [mcp-geoip-server endpoint](https://ip.api4claw.com/mcp)
- [ClawHub skill page](https://clawhub.ai/marc-chen/skills/ip-geo-location-skill)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Concise text and Markdown tables for agent responses; JSON arrays when using the helper script.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses '-' for empty geolocation fields, marks invalid or blocked inputs explicitly, and may return multiple rows for domains with multiple A or AAAA records.]

## Skill Version(s):

0.1.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
