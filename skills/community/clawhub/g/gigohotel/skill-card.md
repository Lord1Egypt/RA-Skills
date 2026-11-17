## Description:

AIGo Hotel Search helps agents search hotels by location, dates, star rating, budget, and tags through the AIGoHotel MCP service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[l18784175468-oss](https://clawhub.ai/user/l18784175468-oss)

### License/Terms of Use:


## Use Case:

External users and travel-focused agents use this skill to search hotels, inspect room prices, and discover available hotel filters while limiting shared data to hotel-search parameters.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Hotel search details such as location, dates, party size, budget, and preferences may be sent to the external AIGoHotel MCP service.

Mitigation: Filter out names, phone numbers, email addresses, identity numbers, local file details, system information, and unrelated free text before calling the MCP tools.

Risk: The bundled public AIGoHotel key may be rate-limited or provide less request attribution than a dedicated key.

Mitigation: Use a dedicated AIGoHotel key when higher quota, operational accountability, or clearer request attribution is required.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/l18784175468-oss/skills/gigohotel)
- [AIGoHotel MCP Service](https://mcp.aigohotel.com/mcp)
- [AIGoHotel API Key Application](https://mcp.aigohotel.com/apply)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown and structured MCP tool-call guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses searchHotels, getHotelDetail, and getHotelSearchTags; hotel queries should exclude personal identifiers.]

## Skill Version(s):

1.0.9 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
