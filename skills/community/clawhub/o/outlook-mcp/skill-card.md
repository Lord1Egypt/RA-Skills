## Description:

Connects AI agents to personal Outlook accounts through typed Microsoft Graph tools for mail, calendar, contacts, tasks, attachments, and related workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mpalermiti](https://clawhub.ai/user/mpalermiti)

### License/Terms of Use:

MIT

## Use Case:

Agent builders use it to read and manage personal Outlook mail, calendars, contacts, tasks, and attachments from an MCP host. It requires a user-configured Azure app and prior CLI authentication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence reports a document-parser isolation weakness for attachment reading.

Mitigation: Keep the opt-in documents toolset disabled unless needed, treat extracted attachment text as untrusted, and verify requested actions with the user.

Risk: The security evidence reports a calendar notification permission gap.

Mitigation: Review granted calendar permissions and require user confirmation before attendee-facing invitations, updates, or cancellations.

Risk: Security scanner coverage was partial, so the assessment may not cover every file or behavior.

Mitigation: Review the installation source, permissions, and release independently before connecting an Outlook account.

## Reference(s):

- [ClawHub release](https://clawhub.ai/mpalermiti/skills/outlook-mcp)
- [PyPI package](https://pypi.org/project/outlook-graph-mcp/)

## Skill Output:

**Output Type(s):** [API Calls, Text, Configuration instructions, Guidance]

**Output Format:** [MCP tool calls with structured or text responses, plus setup guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses depend on the selected Outlook operation and account data.]

## Skill Version(s):

1.33.0 (source: pyproject.toml, CHANGELOG, release evidence; released 2026-11-16)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
