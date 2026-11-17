## Description:

Plaud Recordings to Google Calendar Events scans Plaud recording transcripts for concrete scheduling commitments, resolves dates and times in the user's timezone, creates matching Google Calendar events, and logs processed recordings in Google Sheets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentpmt](https://clawhub.ai/user/agentpmt)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent operators use this skill to turn spoken commitments in Plaud recordings into calendar events while keeping an audit ledger of processed recordings and created events.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Transcript excerpts and recording links can be written into Google Calendar events and Google Sheets ledger rows.

Mitigation: Use the workflow only for recordings whose participants and contents are appropriate for storage in those connected services.

Risk: Connected Plaud and Google accounts may expose sensitive recordings, calendars, or spreadsheets if broad permissions are granted.

Mitigation: Use least-privilege scopes and trusted, verified installation paths for all connected tools.

Risk: Incorrect timezone handling or ambiguous spoken commitments can create wrong calendar events.

Mitigation: Resolve dates against the recording's local date and the user's timezone, and skip vague commitments that do not include a concrete time.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/agentpmt/skills/plaud-recordings-to-google-calendar-events)
- [AgentPMT workflow page](https://www.agentpmt.com/agent-workflow-skills/plaud-recordings-to-google-calendar-events)
- [AgentPMT account MCP/REST setup](https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup)
- [Plaud tool skill](https://clawhub.ai/agentpmt/plaud)
- [Google Calendar tool skill](https://clawhub.ai/agentpmt/google-calendar)
- [Google Sheets tool skill](https://clawhub.ai/agentpmt/google-sheets)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, API calls, markdown]

**Output Format:** [Markdown instructions with JSON and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces agent workflow guidance for Plaud, Google Calendar, Google Sheets, and AgentPMT-hosted tool calls.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
