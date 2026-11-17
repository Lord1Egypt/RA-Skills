## Description:

An intelligent assistant designed to help you plan your cruise vacations seamlessly. Get insights, recommendations, and booking assistance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[309441738](https://clawhub.ai/user/309441738)

### License/Terms of Use:

MIT

## Use Case:

External users use this agent to explore cruise vacation options, retrieve cruise product details, and search cruise products by filters or keywords.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Published instructions include an unrelated httpbin.org POST placeholder that could expose user-provided travel or prompt data.

Mitigation: Remove or replace the placeholder with the confirmed CruiseSkillBridge gateway, and state what user data is sent, to whom, and under what consent controls before installation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/309441738/skills/ola-agent-cruise-planning)
- [CruiseSkillBridge](https://cruiseskillbridge.com)
- [MCP server schema](https://static.modelcontextprotocol.io/schemas/2025-07-09/server.schema.json)

## Skill Output:

**Output Type(s):** [Text, Guidance, API Calls]

**Output Format:** [Markdown or plain text responses with JSON payloads for MCP tool calls]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call CruiseSkillBridge MCP tools for product listing, product detail lookup, and keyword search.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
