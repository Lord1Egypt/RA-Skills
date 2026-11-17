## Description:

Access detailed real estate data including property specifications, sales history, market values, tax assessments, rental estimates, sales trends, and nearby schools through the Pipeworx ATTOM MCP endpoint.

This skill is ready for commercial/non-commercial use.

## Publisher:

[b-gutman](https://clawhub.ai/user/b-gutman)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and real-estate analysts use this skill to connect an agent to ATTOM property lookup tools for property details, comparable searches, sales history, automated valuation, assessments, rental estimates, ZIP-code trends, and nearby school information.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Property addresses, ZIP codes, coordinates, and related real-estate queries are sent to the configured Pipeworx MCP endpoint.

Mitigation: Install only when sharing those query details with the endpoint is acceptable, and avoid sending unnecessary sensitive information.

Risk: Returned valuation, tax, school, sales, and rental information is third-party remote output.

Mitigation: Verify important property data against authoritative sources before relying on it for decisions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/b-gutman/skills/pipeworx-attom)
- [Pipeworx ATTOM MCP Endpoint](https://gateway.pipeworx.io/attom/mcp)

## Skill Output:

**Output Type(s):** [Configuration, Guidance, Text]

**Output Format:** [Markdown with JSON configuration snippets and plain-text real-estate lookup results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns third-party remote property data; verify important valuation, tax, school, and sales information before relying on it.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
