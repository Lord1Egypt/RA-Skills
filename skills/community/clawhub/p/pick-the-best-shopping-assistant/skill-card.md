## Description:

Pick the Best - Personal shopping assistant for product search, price comparison, and recommendations powered by Pick the Best.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nepp-an](https://clawhub.ai/user/nepp-an)

### License/Terms of Use:

MIT-0

## Use Case:

External shoppers use this skill to search for products, compare prices, find deals, and receive shopping recommendations through Pick the Best shopping tools.

### Deployment Geography for Use:

United Kingdom, Germany, Poland, and France

## Known Risks and Mitigations:

Risk: Shopping requests and session identifiers may be sent to Pick the Best.

Mitigation: Use the skill only for intentional shopping requests, avoid sensitive personal details, and do not use usernames, emails, account IDs, or other stable identifiers as session_id values.

Risk: Product links may contain affiliate tracking.

Mitigation: Make users aware that product links can include tracking before they open or share links.

Risk: Ambiguous market requests may default to GB.

Mitigation: Ask for or explicitly set the market when the user's location, country, or currency is unclear.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nepp-an/skills/pick-the-best-shopping-assistant)
- [Pick the Best shopping MCP endpoint](https://pickthebest.com/gb/en/v1/shopping/mcp)
- [Model Context Protocol Specification](https://modelcontextprotocol.io/)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with product summaries, shopping links, and JSON-RPC curl examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include product links with affiliate tracking; unclear markets may default to GB.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
