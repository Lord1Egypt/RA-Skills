## Description:

Local Business Discovery and Mapping: Search for nearby places or by text query. 30+ category filters. Use when an agent needs local business discovery and mapping, local business discovery and recommendations for travel planning, restaurant and dining venue search for meal planning applications, healthcare facility location for medical service directories, retail store finding for shopping assistance, geocode, address, nearby search through AgentPMT-hosted remote tool calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentpmt](https://clawhub.ai/user/agentpmt)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agents use this skill to discover local businesses and places, geocode addresses, reverse geocode coordinates, and run location-biased text searches through AgentPMT-hosted remote tool calls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Location searches can expose sensitive home, workplace, or other precise addresses to a remote service.

Mitigation: Send only the minimum location detail needed for the task and avoid using sensitive addresses unless required.

Risk: Remote setup and invocation may involve account credentials or payment-related headers.

Mitigation: Use the referenced setup flow for credential handling and do not place AgentPMT credentials, wallet secrets, signatures, or payment headers in prompts or logs.

Risk: Endpoint details, schemas, or examples may change after publication.

Mitigation: Refresh the installed skill or fetch live schema and instructions before new production integrations or unclear calls.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/agentpmt/skills/local-business-discovery-and-mapping)
- [AgentPMT Marketplace Page](https://www.agentpmt.com/marketplace/local-business-discovery-and-mapping)
- [Action Schema](artifact/schema.md)
- [AgentPMT MCP Server](https://api.agentpmt.com/mcp/)
- [AgentPMT REST Invoke Endpoint](https://api.agentpmt.com/products/purchase)

## Skill Output:

**Output Type(s):** [guidance, configuration, shell commands, API calls]

**Output Format:** [Markdown instructions with JSON request examples and schema references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports geocode, nearby_search, reverse_geocode, and text_search action guidance; remote tool responses are JSON.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
