## Description:

Tuniu Hotel Booking Skill helps agents search Tuniu hotels, review hotel details and room quotes, and create booking orders through the Tuniu hotel MCP service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leonardoooooo](https://clawhub.ai/user/leonardoooooo)

### License/Terms of Use:

MIT-0

## Use Case:

External travel users and agent operators use this skill to search hotels by city and date, inspect hotel details and room rates, and create hotel booking orders after user confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create real hotel booking orders using user-provided guest and contact details.

Mitigation: Require clear final confirmation of the hotel, room, dates, price, guest names, and phone number before submitting an order.

Risk: API keys and personal booking details are sent through curl requests, and a custom MCP URL could route sensitive data to an unintended endpoint.

Mitigation: Keep TUNIU_MCP_URL unset or pinned to https://openapi.tuniu.cn/mcp/hotel, use a narrowly scoped rotatable Tuniu API key, and avoid logging or displaying API keys and personal information.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/leonardoooooo/skills/hotelclaw)
- [Tuniu Open Platform MCP](https://open.tuniu.com/mcp)
- [Tuniu hotel MCP endpoint](https://openapi.tuniu.cn/mcp/hotel)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown responses with inline curl commands and JSON response-handling guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and TUNIU_API_KEY; booking flows handle hotel search results, room details, order identifiers, payment links, and user-provided booking details.]

## Skill Version(s):

1.0.4 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
