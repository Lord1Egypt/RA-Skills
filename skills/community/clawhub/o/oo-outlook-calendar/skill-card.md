## Description:

Outlook Calendar (microsoft.com). Use this skill for ANY Outlook Calendar request — reading, creating, updating, and deleting data. Whenever a task involves Outlook Calendar, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to read calendars and availability, manage invitations, find meeting times, and create or manage Outlook events through a connected account. It requires user approval for calendar changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup instructs the agent to run a downloaded oo CLI installer that has not been verified.

Mitigation: Review and approve CLI installation separately, preferably using a pinned, verified release.

Risk: Connecting Outlook entrusts OOMOL with calendar access, and write actions can change or remove events.

Mitigation: Confirm the connected account and permissions, and retain the skill's approval requirements for calendar changes.

## Reference(s):

- [Outlook Calendar](https://www.microsoft.com/microsoft-365/outlook/outlook-calendar)
- [Microsoft Graph calendar resource](https://learn.microsoft.com/en-us/graph/api/resources/calendar)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Text]

**Output Format:** [Text responses with JSON connector requests and responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Calendar changes require user approval; destructive changes require explicit approval.]

## Skill Version(s):

1.0.2 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
