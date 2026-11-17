## Description:

Connects agents to a Pipeworx-hosted CFPB MCP endpoint for searching and retrieving Consumer Financial Protection Bureau complaint data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[b-gutman](https://clawhub.ai/user/b-gutman)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to query CFPB consumer complaint data through a Pipeworx-hosted MCP gateway, including complaint search, company complaint lookup, complaint detail retrieval, top-company rankings, and product breakdowns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms and complaint queries are routed through a third-party Pipeworx MCP gateway rather than directly to an official CFPB endpoint.

Mitigation: Avoid confidential personal or financial details in search terms and treat returned data as mediated by the gateway.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/b-gutman/skills/pipeworx-cfpb)
- [Pipeworx CFPB MCP gateway](https://gateway.pipeworx.io/cfpb/mcp)

## Skill Output:

**Output Type(s):** [text, configuration, guidance]

**Output Format:** [Markdown guidance with JSON MCP server configuration and text complaint data returned by MCP tools]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Routes CFPB complaint searches through a third-party MCP gateway; returned data may include complaint narratives, company responses, rankings, and product category breakdowns.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
