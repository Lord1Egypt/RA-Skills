## Description:

Manage Outlook and Microsoft 365 calendar events, recurring events, reminders, and free-time queries through an agent-run Python CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lovely-qianyun](https://clawhub.ai/user/lovely-qianyun)

### License/Terms of Use:

MIT

## Use Case:

People using Outlook calendar with an AI agent use this skill to inspect availability and manage events on a connected default calendar after signing in through Microsoft Graph.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can modify a signed-in Outlook calendar through calendar-write OAuth permissions.

Mitigation: Verify the intended account with status before writes, use a separate token path for isolated sessions, and revoke Microsoft consent when access is no longer needed.

Risk: Normal calendar use can automatically install unpinned Python dependencies.

Mitigation: Run the skill in a dedicated Python environment and preinstall or pin requests, msal, and tzdata before use.

Risk: Calendar actions depend on correctly normalized dates, times, recurrence scope, and timezone.

Mitigation: Resolve relative language into explicit values before writes, preserve those values for retries, and read back or query the target window to verify the requested result.

## Reference(s):

- [Command reference](references/commands.md)
- [Configuration and permissions](references/configuration.md)
- [Recurring events guide](references/recurring-events.md)
- [Troubleshooting guide](references/troubleshooting.md)
- [Azure app setup](references/azure-app-setup.md)
- [Microsoft Graph recurrence pattern types](https://learn.microsoft.com/en-us/graph/api/resources/recurrencepattern?view=graph-rest-1.0)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON operation contracts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Calendar commands can return one JSON value on stdout with diagnostics on stderr.]

## Skill Version(s):

3.0.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
