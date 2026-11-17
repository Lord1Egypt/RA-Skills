## Description:

Provides practical cruise travel advice, including preparation tips, best departure timing, and destination recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[309441738](https://clawhub.ai/user/309441738)

### License/Terms of Use:

MIT

## Use Case:

External users and travel-planning agents use this MCP skill to request practical cruise guidance and retrieve cruise product details by product number through the published product_info tool.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Remote MCP behavior is under-specified and routed through an external gateway.

Mitigation: Review the real endpoint, available tool schemas, and data-handling policy before enabling the skill in customer or production workflows.

Risk: Travel requests could include personal, payment, booking, credential, or itinerary details.

Mitigation: Do not send sensitive travel or account data through the documented example endpoint or remote MCP tools until the publisher documents handling and retention practices.

Risk: The artifact includes placeholder capability text and security evidence notes that some data flows are unrelated to the advertised purpose.

Mitigation: Validate the product_info tool behavior and review returned advice before relying on the skill for commercial travel planning.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/309441738/skills/ola-cp-travel-advice)
- [MCP Server Access](artifact/references/mcp.md)
- [CruiseSkillBridge](https://cruiseskillbridge.com)

## Skill Output:

**Output Type(s):** [Text, Guidance, API Calls, Configuration]

**Output Format:** [Markdown guidance and JSON MCP/API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May route requests through a remote MCP gateway.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
