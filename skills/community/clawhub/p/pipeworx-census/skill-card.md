## Description:

Access U.S. Census Bureau housing data including ACS, building permits, housing starts, homeownership rates, and available census datasets by geography.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brucegutman](https://clawhub.ai/user/brucegutman)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to query Census housing datasets through a Pipeworx MCP server for geography-specific ACS, permit, construction, homeownership, and dataset-discovery results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Census-related queries are sent through the third-party gateway at gateway.pipeworx.io.

Mitigation: Confirm the gateway is acceptable for the intended use before installing or invoking the skill.

Risk: Returned Census values may be incomplete, unavailable, or unsuitable for high-stakes decisions without verification.

Mitigation: Verify important results against official Census sources when accuracy matters.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/brucegutman/skills/pipeworx-census)
- [Pipeworx Census MCP gateway](https://gateway.pipeworx.io/census/mcp)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration, Guidance]

**Output Format:** [Markdown with Census query results and MCP configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses depend on availability and behavior of the third-party Pipeworx gateway and underlying Census data sources.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
