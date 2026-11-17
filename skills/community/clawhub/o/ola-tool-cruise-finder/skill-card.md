## Description:

A powerful tool that assists users in finding the best cruises based on their preferences and requirements.

This skill is ready for commercial/non-commercial use.

## Publisher:

[309441738](https://clawhub.ai/user/309441738)

### License/Terms of Use:

MIT

## Use Case:

External users and travel-support agents use this skill to search for cruise products by keyword and find cruises that match user preferences.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill documentation includes an HTTPBin testing endpoint for submitted user input.

Mitigation: Do not send sensitive travel details, payment data, identity documents, or private contact information until the publisher documents the production endpoint and data handling practices.

Risk: The remote gateway uses metering and may process user queries outside the local agent environment.

Mitigation: Review the gateway service, logging, retention, and deletion practices before installing or using the skill in production.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/309441738/skills/ola-tool-cruise-finder)
- [Publisher profile](https://clawhub.ai/user/309441738)
- [CruiseSkillBridge](https://cruiseskillbridge.com)
- [Model Context Protocol server schema](https://static.modelcontextprotocol.io/schemas/2025-07-09/server.schema.json)

## Skill Output:

**Output Type(s):** [text, API calls, guidance]

**Output Format:** [JSON or text returned from remote cruise product search tools]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a remote streamable HTTP MCP endpoint; avoid sensitive travel, payment, identity, or contact data unless production privacy practices are documented.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact frontmatter and server.json show 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
