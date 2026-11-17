## Description:

Check whether major websites and online services are down, list confirmed outages, find reporting spikes, and retrieve measured uptime through the IsItDown.now API. Use for current service-status or outage-history questions; do not use it to diagnose a user's private network or to claim that one external measurement is conclusive.

This skill is ready for commercial/non-commercial use.

## Publisher:

[henrick86](https://clawhub.ai/user/henrick86)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to check monitored website availability, identify confirmed outages or report spikes, and review recent uptime and incident history using IsItDown.now's read-only measurements.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An API key could be exposed, and queried service identifiers are received by IsItDown.now.

Mitigation: Keep the key in a secret store or environment and never in chat; consider the provider's receipt of queried identifiers before use.

Risk: An external availability measurement may not reflect the user's local connection or the service provider's official status.

Mitigation: State when the measurement was taken and check the affected service's official status page before consequential decisions.

## Reference(s):

- [IsItDown.now](https://isitdown.now)
- [IsItDown.now read-only MCP server](https://mcp.isitdown.now)
- [ClawHub skill release](https://clawhub.ai/henrick86/skills/isitdown-now)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Concise status summaries with measurement timestamps and source links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Distinguishes confirmed outages from report spikes and external measurements from official status or uptime guarantees.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
