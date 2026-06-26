## Description: <br>
Schedule and book meetings through the Meet.bot MCP server, including availability checks, booking links, and confirmed bookings that require a Meet.bot API key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[poolside-ventures](https://clawhub.ai/user/poolside-ventures) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to list scheduling pages, check open time slots, share booking links, and book meetings with confirmed guest details. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Meet.bot API key for authenticated MCP server calls. <br>
Mitigation: Verify the endpoint is the intended Meet.bot service and use an appropriate or revocable API key where possible. <br>
Risk: The skill can book meetings, and cancellation is not available through this server. <br>
Mitigation: Review meeting page, guest details, and start time with the user before approving a booking. <br>


## Reference(s): <br>
- [Meet.bot MCP server](https://mcp.meet.bot) <br>
- [ClawHub skill page](https://clawhub.ai/poolside-ventures/meetbot) <br>
- [Publisher profile](https://clawhub.ai/user/poolside-ventures) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown or concise text with meeting options, booking confirmations, and booking links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include local-time availability summaries, confirmed meeting details, and Meet.bot booking links.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
