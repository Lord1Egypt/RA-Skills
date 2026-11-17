## Description:

Provides national and local housing market analysis by combining FRED, BLS, ATTOM, and HUD data for property and market insights.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brucegutman](https://clawhub.ai/user/brucegutman)

### License/Terms of Use:

MIT-0

## Use Case:

Real estate analysts, housing researchers, and agents use this skill to query housing-market indicators, property details, rental estimates, affordability signals, and local sales trends across supported data sources.

### Deployment Geography for Use:

Global, with U.S.-focused housing data sources

## Known Risks and Mitigations:

Risk: Sensitive property queries may include street addresses, ownership-linked records, valuations, or coordinates routed through a third-party MCP gateway.

Mitigation: Share only necessary property details with the gateway and avoid submitting unnecessary personal or property-identifying information.

Risk: Property-specific findings may be retained if memory tools are used without clear user intent.

Mitigation: Do not save property-specific findings in memory unless the user explicitly requests retention.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/brucegutman/skills/pipeworx-housing-analyst)
- [Publisher profile](https://clawhub.ai/user/brucegutman)
- [Pipeworx Housing Intel MCP endpoint](https://gateway.pipeworx.io/mcp?task=housing%20analysis)

## Skill Output:

**Output Type(s):** [Text, Markdown, API calls, Guidance]

**Output Format:** [Markdown or text summaries backed by MCP tool results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include housing indicators, property characteristics, valuations, rental estimates, affordability checks, and sales trends.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
