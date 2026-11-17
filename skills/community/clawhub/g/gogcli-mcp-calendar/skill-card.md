## Description:

Use when the user asks to manage Google Calendar events or Google Meet spaces. Triggers for scheduling, listing events, creating/updating/deleting events, responding to invitations, creating Meet spaces, ending conferences, listing meeting participants or call history.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chrischall](https://clawhub.ai/user/chrischall)

### License/Terms of Use:

MIT

## Use Case:

Calendar users and meeting organizers use an agent to review schedules, create or update events, respond to invitations, and manage Google Meet spaces and calls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review flags broader actions alongside Calendar and Meet, including whole-calendar deletion and Zoom credential management.

Mitigation: Review the permissions and tools before enabling the skill, limit Google scopes, use read-only mode where possible, and enable deletion or Zoom credential tools only when needed.

Risk: The security review reports partial scan coverage and unverified dependency versions.

Mitigation: Review the source and dependency versions before connecting the skill to an account with sensitive calendar data.

## Reference(s):

- [gogcli project](https://github.com/openclaw/gogcli)
- [Model Context Protocol](https://modelcontextprotocol.io)
- [ClawHub skill listing](https://clawhub.ai/chrischall/skills/gogcli-mcp-calendar)

## Skill Output:

**Output Type(s):** [API Calls, Text, Configuration]

**Output Format:** [Structured text and JSON tool responses, with configuration examples in Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Calendar event and meeting information or requested changes, depending on the operation.]

## Skill Version(s):

4.12.0 (source: package.json, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
