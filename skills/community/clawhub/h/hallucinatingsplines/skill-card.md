## Description:

Build and manage cities autonomously on Hallucinating Splines, a headless Micropolis simulator with a REST API and MCP server for AI agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[andrewedunn](https://clawhub.ai/user/andrewedunn)

### License/Terms of Use:


## Use Case:

Developers and agent builders use this skill to connect agents to the Hallucinating Splines game service, create simulated cities, inspect city state, and take autonomous city-management actions through the REST API or MCP server.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An autonomous loop can repeatedly create, modify, advance, budget, or retire simulated cities through the remote game service.

Mitigation: Run continuous loops only when those remote game actions are intended, and monitor city activity with the heartbeat checks.

Risk: The service API key enables agent actions against Hallucinating Splines cities.

Mitigation: Keep HS_API_KEY scoped to this service, store it as a secret, and revoke it when it is no longer needed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/andrewedunn/skills/hallucinatingsplines)
- [Hallucinating Splines Home](https://hallucinatingsplines.com)
- [Skill Source](https://hallucinatingsplines.com/skill.md)
- [Heartbeat Guide](https://hallucinatingsplines.com/heartbeat.md)
- [API Base](https://api.hallucinatingsplines.com/v1)
- [MCP Server](https://mcp.hallucinatingsplines.com/mcp)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, API Calls, Configuration]

**Output Format:** [Markdown with shell, JSON, and Python examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an HS_API_KEY scoped to the Hallucinating Splines service.]

## Skill Version(s):

1.0.2 (source: ClawHub release metadata; artifact frontmatter lists 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
