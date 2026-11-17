## Description:

Connect to nAIm, a machine-first API registry for AI agents, to browse services, search by category, compare pricing and authentication types, and rate APIs through MCP SSE.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aiall-tars](https://clawhub.ai/user/aiall-tars)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to connect agents to the nAIm registry, discover API services by category or constraints, inspect ratings, and submit ratings for services they have used.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries, agent identifiers, and rating notes are sent to an external MCP service.

Mitigation: Avoid including secrets, private tenant names, sensitive internal system identifiers, or proprietary operational details in queries, agent_id values, or notes.

Risk: Service listings and community ratings may not be sufficient to approve an API for a production workflow.

Mitigation: Review candidate API providers, pricing, authentication, reliability, and policy requirements before adoption.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aiall-tars/skills/naim-mcp)
- [nAIm homepage](https://naim.janis7ewski.org)
- [nAIm API endpoint](https://api.naim.janis7ewski.org)
- [nAIm MCP SSE endpoint](https://mcp.naim.janis7ewski.org/sse)

## Skill Output:

**Output Type(s):** [Text, Configuration, Guidance]

**Output Format:** [Markdown with JSON configuration and MCP tool-call examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Connects to an external MCP SSE service; no API key is required by the skill documentation.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
