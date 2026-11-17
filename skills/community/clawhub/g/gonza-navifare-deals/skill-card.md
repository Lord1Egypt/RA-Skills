## Description:

Verify and compare flight prices across multiple booking sites using Navifare when users share flight prices from booking sites or upload flight screenshots, returning ranked results with booking links from multiple providers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gonzachee](https://clawhub.ai/user/gonzachee)

### License/Terms of Use:

MIT-0

## Use Case:

External travelers and travel-support agents use this skill to validate a quoted round-trip flight price, search comparable booking sources through the Navifare MCP service, and present ranked options with savings guidance and booking links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Flight itinerary details and reference prices are sent to Navifare's hosted MCP service.

Mitigation: Confirm the user is comfortable sharing pre-booking itinerary data before search, and avoid sending passenger names, booking references, passport details, loyalty numbers, payment data, or other personal information.

Risk: Screenshots from booking sites may contain personal or booking information beyond the itinerary.

Mitigation: Extract only flight numbers, airlines, airports, dates, times, travel class, passenger count, reference price, and currency before calling the Navifare MCP tools.

Risk: Flight prices and availability may change after the search completes.

Mitigation: Present prices as time-sensitive comparison results and direct users to verify final fare details, restrictions, and provider terms before purchase.

Risk: The skill depends on a hosted MCP endpoint and may return no results, partial results, or time out.

Mitigation: Explain MCP availability issues clearly, use partial results when available, and ask the user to verify flight details before retrying.

Risk: Optional global npm validation can install executable tooling outside the skill artifact.

Mitigation: Skip the optional global npm validation command unless the package version is pinned and trusted.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gonzachee/skills/gonza-navifare-deals)
- [Navifare MCP documentation](https://www.navifare.com/mcp)
- [Navifare MCP endpoint](https://mcp.navifare.com/mcp)
- [AgentSkills specification](https://agentskills.io/specification)
- [Airport code reference](references/AIRPORTS.md)
- [Airline code reference](references/AIRLINES.md)
- [Usage examples](references/EXAMPLES.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, API calls, Configuration, Guidance]

**Output Format:** [Markdown summaries with comparison tables, savings calculations, booking links, and MCP request/response guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on Navifare MCP availability and may include partial results when a search times out.]

## Skill Version(s):

1.2.2 (source: server release metadata; artifact frontmatter version is 1.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
