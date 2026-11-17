## Description:

An AI chat bot designed to assist users in finding and booking cruise products right from their chat interface.

This skill is ready for commercial/non-commercial use.

## Publisher:

[309441738](https://clawhub.ai/user/309441738)

### License/Terms of Use:

MIT

## Use Case:

External users use this agent to search, compare, and request details about cruise products in a chat interface, including filters such as brand, departure city, destination, price, trip length, ship, and date.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Security review marked the release suspicious because the skill text directs user input to an unrelated httpbin.org testing endpoint.

Mitigation: Review endpoint behavior before installation and avoid sending personal details, contact information, payment data, or sensitive travel plans unless the publisher removes or clearly replaces that endpoint.

Risk: The hosted gateway's data handling and retention are not documented in the provided evidence.

Mitigation: Confirm what data the hosted gateway receives and retains before using the skill with booking or travel-planning data.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/309441738/skills/ola-cruise-chat-bot)
- [Publisher Profile](https://clawhub.ai/user/309441738)
- [CruiseSkillBridge](https://cruiseskillbridge.com)
- [Model Context Protocol Server Schema](https://static.modelcontextprotocol.io/schemas/2025-07-09/server.schema.json)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Chat responses with cruise product listings, product details, and search guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use hosted MCP tools for product listing, product detail lookup, and keyword search.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact frontmatter and server.json report 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
