## Description: <br>
Intelligent hotel search that supports filtering by place, date, star rating, budget, and tags. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[l18784175468-oss](https://clawhub.ai/user/l18784175468-oss) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and travel-assistant agents use this skill to search for hotels, inspect room pricing, and discover hotel filter tags through the AIGoHotel MCP service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Hotel search criteria are sent to the AIGoHotel MCP service. <br>
Mitigation: Send only search-relevant fields such as location, dates, budget, guest counts, and preferences. <br>
Risk: User prompts may contain personal information unrelated to hotel search. <br>
Mitigation: Remove names, phone numbers, emails, ID numbers, and unrelated personal details before setting originQuery or calling hotel tools. <br>
Risk: The bundled public API key may be rate limited. <br>
Mitigation: Use the public key for normal access and apply for a dedicated key when higher quota is required. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/l18784175468-oss/gigohotel) <br>
- [AIGoHotel MCP endpoint](https://mcp.aigohotel.com/mcp) <br>
- [AIGoHotel API key application](https://mcp.aigohotel.com/apply) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, API calls, configuration, text] <br>
**Output Format:** [Markdown guidance with JSON MCP configuration and structured hotel results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include hotel lists, room prices, cancellation policies, and categorized search tags.] <br>

## Skill Version(s): <br>
1.0.9 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
