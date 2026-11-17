## Description:

Provides country, state, and city lookup data including ISO codes, capitals, phone codes, currencies, regions, states, provinces, and cities through a hosted Pipeworx CountryStateCity MCP connector.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brucegutman](https://clawhub.ai/user/brucegutman)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to retrieve country, state or province, and city reference data for location-aware workflows, validation, enrichment, and user-facing geographic lookups.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Country, state, and city queries are sent to an external hosted MCP endpoint.

Mitigation: Use the connector only when sending those lookup queries to the hosted service is acceptable for the workflow.

Risk: The remote service can change independently of this reviewed artifact.

Mitigation: Review the configured endpoint and service behavior before deployment and during periodic security reviews.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/brucegutman/skills/pipeworx-country-state-city)
- [Hosted MCP endpoint](https://gateway.pipeworx.io/country-state-city/mcp)
- [CountryStateCity API endpoint](https://api.countrystatecity.in/v1)

## Skill Output:

**Output Type(s):** [text, configuration, API calls]

**Output Format:** [Markdown descriptions, JSON MCP configuration, and lookup responses from the hosted MCP service]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the hosted MCP endpoint and the upstream CountryStateCity API.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
