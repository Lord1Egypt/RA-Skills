## Description: <br>
Helps agents search Tuniu hotels, retrieve hotel details, and create hotel booking orders through the Tuniu MCP service. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leonardoooooo](https://clawhub.ai/user/leonardoooooo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Travel users and booking agents use this skill to search for hotels by city and dates, inspect room and rate details, and submit confirmed hotel booking orders. The skill requires a Tuniu API key and uses curl to call the Tuniu MCP endpoint. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create hotel booking orders and send contact or guest personal information to the Tuniu MCP service. <br>
Mitigation: Before any create-order call, show the final hotel, room, dates, price-relevant details, contact, and guest summary, then require explicit user confirmation. <br>
Risk: The skill requires a Tuniu API key and uses curl to call an external MCP endpoint. <br>
Mitigation: Install only when the Tuniu MCP service is trusted, keep TUNIU_API_KEY out of replies and logs, and review the curl request before execution. <br>


## Reference(s): <br>
- [Tuniu Open Platform MCP](https://open.tuniu.com/mcp) <br>
- [ClawHub skill page](https://clawhub.ai/leonardoooooo/hotelclaw) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown or plain text summaries with curl commands and parsed JSON-RPC response guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and TUNIU_API_KEY; booking calls may send contact and guest personal information to the Tuniu MCP service, so agents should show a final order summary and get explicit confirmation before creating an order.] <br>

## Skill Version(s): <br>
1.0.4 (source: target metadata, evidence release, artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
