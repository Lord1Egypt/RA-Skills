## Description: <br>
LeafEngines provides agricultural intelligence tools for soil analysis, crop recommendations, and TurboQuant capability checks through a hosted MCP service. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qwarranto](https://clawhub.ai/user/qwarranto) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and agents use this skill to query LeafEngines' hosted agricultural service for county-level soil analysis, crop recommendations, and TurboQuant availability checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agricultural queries, county or location data, and paid API headers are sent to a hosted LeafEngines service. <br>
Mitigation: Use the free-tier header for evaluation, avoid unnecessary sensitive farm or business details, and store paid keys only in MCP header or secret configuration. <br>
Risk: The public test key and free-tier access should be treated as public and revocable. <br>
Mitigation: Do not rely on the public test key for private or production workflows; use a paid key managed through secret storage when higher trust or continuity is required. <br>
Risk: The artifact includes an install script that changes local OpenClaw configuration. <br>
Mitigation: Review scripts/install.sh before execution and confirm the target MCP endpoint and headers match the intended deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/qwarranto/leafengines) <br>
- [Publisher profile](https://clawhub.ai/user/qwarranto) <br>
- [LeafEngines MCP homepage](https://app.soilsidekickpro.com/mcp) <br>
- [MCP server endpoint](https://wzgnxkoeqzvueypwzvyn.supabase.co/functions/v1/mcp-server) <br>
- [API reference](references/API_REFERENCE.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown guidance with MCP configuration snippets and hosted API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses county FIPS codes and optional authentication headers for paid features.] <br>

## Skill Version(s): <br>
1.1.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
