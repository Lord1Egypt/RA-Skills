## Description:

Sets up Nodo over MCP so an agent can work in logged-in websites through a cloud Chrome session that stays signed in.

This skill is ready for commercial/non-commercial use.

## Publisher:

[otto-iron](https://clawhub.ai/user/otto-iron)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent operators use this skill to complete recurring work in authorized logged-in websites that do not provide a suitable API, such as supplier portals, marketplaces, and dashboards.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The cloud browser retains signed-in website sessions, while the remote setup contents and credential-storage claims have not been verified.

Mitigation: Review setup instructions and access permissions before connecting, use only authorized accounts, and explicitly approve recurring workflows.

## Reference(s):

- [Nodo MCP setup instructions](https://mcp.nodo.com/start.md)
- [Nodo website](https://nodo.com)
- [ClawHub release page](https://clawhub.ai/otto-iron/skills/nodo-logged-in-browser)

## Skill Output:

**Output Type(s):** [Text, Browser interactions, Configuration instructions]

**Output Format:** [Text responses and website actions through a logged-in browser session]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Recurring workflow setup requires explicit user approval.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
