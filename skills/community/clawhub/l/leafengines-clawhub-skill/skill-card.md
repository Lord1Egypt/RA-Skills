## Description: <br>
LeafEngines provides an MCP-based agricultural intelligence API for Claude and OpenClaw, including soil analysis, weather forecasting, crop recommendations, environmental compliance, planting optimization, carbon credit calculation, and TurboQuant capability checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qwarranto](https://clawhub.ai/user/qwarranto) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Farmers, agricultural advisors, researchers, students, developers, and AI agents use this skill to connect to LeafEngines for agricultural planning, soil and weather analysis, crop selection, irrigation support, yield estimation, market data, sustainability scoring, and TurboQuant capability checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends API-key authenticated agricultural, location, and possibly image or farm planning data to a remote LeafEngines service. <br>
Mitigation: Install only if you trust the LeafEngines provider, use a dedicated revocable API key, and avoid sending unnecessary precision, sensitive photos, or confidential farm data. <br>
Risk: LeafEngines is a commercial API service with pricing, quotas, and subscription-tier rate limits. <br>
Mitigation: Review current pricing and quota terms before use, monitor API usage, and choose the lowest required subscription tier. <br>
Risk: Leaving the MCP server configured after use can continue exposing agents to the remote service and stored API key. <br>
Mitigation: Remove the MCP configuration entry and revoke or rotate the API key when the service is no longer needed. <br>


## Reference(s): <br>
- [LeafEngines API Reference](references/API_REFERENCE.md) <br>
- [LeafEngines ClawHub Listing](https://clawhub.ai/qwarranto/leafengines-clawhub-skill) <br>
- [LeafEngines GitHub Project](https://github.com/QWarranto/leafengines-claude-mcp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, API calls] <br>
**Output Format:** [Markdown guidance, YAML configuration snippets, shell commands, and API-backed MCP tool responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a remote MCP/API service with an x-api-key header and subscription-tier rate limits.] <br>

## Skill Version(s): <br>
1.1.0 (source: server evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
