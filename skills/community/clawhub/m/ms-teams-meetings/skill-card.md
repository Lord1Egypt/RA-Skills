## Description:

Create, list, and cancel Microsoft Teams online meetings with calendar invites using your Microsoft 365 account via the Microsoft Graph API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pingukim225](https://clawhub.ai/user/pingukim225)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and developers use this skill to schedule, list, and cancel Teams-enabled Outlook or Exchange calendar events from an agent using their Microsoft 365 account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses Microsoft delegated calendar permissions and local OAuth tokens.

Mitigation: Review the requested Microsoft Graph scopes before use, store tokens only in the intended local path with restrictive permissions, and remove tokens when access is no longer needed.

Risk: The helper code can automatically install unpinned Python packages.

Mitigation: Install dependencies yourself in an isolated environment with pinned versions before running the skill.

Risk: The cancellation helper includes a hard-delete option for calendar events.

Mitigation: Confirm the event ID and attendee impact before cancellation, and treat hard delete as a permanent action.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pingukim225/skills/ms-teams-meetings)
- [Publisher profile](https://clawhub.ai/user/pingukim225)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON outputs from helper scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Created meetings return event IDs, join URLs, web links, attendee data, and calendar timing details; listing and cancellation scripts return JSON.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
