## Description:

Schedule and book meetings using the Meet.bot MCP server by checking calendar availability, finding open slots, booking guest meetings, sharing booking links, and listing scheduling pages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[poolside-ventures](https://clawhub.ai/user/poolside-ventures)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to coordinate Meet.bot scheduling workflows, including checking availability, sharing booking links, and booking meetings after user confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a user-provided Meet.bot API key for scheduling actions.

Mitigation: Install only when the agent is intended to use that API key, and provide the key only through the expected Bearer-token configuration.

Risk: Meetings booked through this server cannot be cancelled through the same server.

Mitigation: Review page URL, guest name, guest email, and start time before approving any booking.

## Reference(s):

- [Meet.bot MCP server](https://mcp.meet.bot)
- [ClawHub Meet.bot skill page](https://clawhub.ai/poolside-ventures/skills/meetbot)
- [Publisher profile](https://clawhub.ai/user/poolside-ventures)

## Skill Output:

**Output Type(s):** [guidance, markdown, API Calls]

**Output Format:** [Markdown and tool-call guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a user-provided Meet.bot API key and user confirmation before booking meetings.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
