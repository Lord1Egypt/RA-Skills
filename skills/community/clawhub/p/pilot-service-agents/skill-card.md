## Description:

Pilot Service Agents helps agents discover and query a Pilot Protocol catalog of always-on service agents that wrap real-world data APIs without requiring caller-managed API keys or direct HTTP integration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teoslayer](https://clawhub.ai/user/teoslayer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to discover available Pilot Protocol service agents, inspect their filter contracts, and request structured data from upstream APIs through pilotctl.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queries and filters may be sent to Pilot Protocol service agents and, for some calls, Gemini-backed or upstream API services.

Mitigation: Do not include secrets, credentials, regulated data, or confidential internal context unless the data flow has been approved.

Risk: Remote service-agent responses may depend on upstream API availability, rate limits, caching, or stale fallback behavior.

Mitigation: Check response metadata and validate important results against the relevant upstream source before relying on them for high-impact decisions.

## Reference(s):

- [Pilot Protocol](https://pilotprotocol.network)
- [ClawHub Skill Page](https://clawhub.ai/teoslayer/skills/pilot-service-agents)
- [Pilot Skills Index](https://teoslayer.github.io/pilot-skills/)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Text, JSON]

**Output Format:** [Markdown guidance with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses depend on Pilot Protocol service agents, upstream API availability, and asynchronous inbox delivery.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
