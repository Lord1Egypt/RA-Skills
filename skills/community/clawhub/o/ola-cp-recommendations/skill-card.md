## Description:

Recommends cruise products based on user preferences and prior choices to help identify suitable sailing options.

This skill is ready for commercial/non-commercial use.

## Publisher:

[309441738](https://clawhub.ai/user/309441738)

### License/Terms of Use:

MIT

## Use Case:

External users and travel-planning agents use this MCP skill to search for and recommend cruise products from stated preferences or search keywords.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cruise search terms or preference details are sent to a hosted CruiseSkillBridge/Ola Vacations MCP gateway.

Mitigation: Use only non-sensitive travel preferences unless the publisher documents data handling and the user has approved sharing.

Risk: The skill is under-documented and includes placeholder capability text.

Mitigation: Review the MCP endpoint, requested fields, and tool behavior before deploying it in workflows involving personal identifiers, detailed travel history, account data, or payment data.

## Reference(s):

- [MCP Server 接入](references/mcp.md)
- [ClawHub Skill Page](https://clawhub.ai/309441738/skills/ola-cp-recommendations)
- [CruiseSkillBridge](https://cruiseskillbridge.com)

## Skill Output:

**Output Type(s):** [Text, Guidance, API Calls]

**Output Format:** [Markdown or plain text recommendations with MCP tool responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses the hosted CruiseSkillBridge/Ola Vacations MCP gateway for product_search.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
