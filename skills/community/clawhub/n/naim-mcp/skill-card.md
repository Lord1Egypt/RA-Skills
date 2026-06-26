## Description: <br>
Connect to nAIm — the machine-first API registry for AI agents. Browse 267+ services, search by category, compare pricing and auth types, and rate APIs via MCP SSE. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aiall-tars](https://clawhub.ai/user/aiall-tars) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to connect an agent to the nAIm API registry, discover services by category or search filters, compare pricing and authentication models, and submit service ratings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Queries, service lookups, ratings, agent_id values, notes, and connection metadata are shared with the remote nAIm MCP service. <br>
Mitigation: Use the skill only with a trusted nAIm endpoint and avoid submitting secrets, sensitive internal details, or confidential usage notes. <br>


## Reference(s): <br>
- [nAIm Homepage](https://naim.janis7ewski.org) <br>
- [nAIm API](https://api.naim.janis7ewski.org) <br>
- [nAIm MCP SSE Endpoint](https://mcp.naim.janis7ewski.org/sse) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Configuration, API Calls, Text] <br>
**Output Format:** [Markdown with JSON configuration and MCP tool call examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces registry search, service lookup, rating lookup, and rating submission guidance through a remote MCP server.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
