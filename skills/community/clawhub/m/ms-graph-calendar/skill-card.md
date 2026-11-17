## Description:

Find available meeting times and free/busy slots for company employees using Microsoft Graph API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[artisong](https://clawhub.ai/user/artisong)

### License/Terms of Use:


## Use Case:

Employees and scheduling assistants use this skill to resolve employee identities, check calendar availability, and suggest meeting times across Microsoft Graph calendars.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Organization-wide Microsoft Graph application access can expose employee directory data and detailed calendar metadata.

Mitigation: Install only after administrator approval, and restrict the application to specific mailboxes before use.

Risk: Credentials or tokens used with this version may be exposed through setup flows or local token handling.

Mitigation: Rotate any secret or token that may have been used, and avoid running setup commands in a way that leaves secrets in command-line history.

Risk: Users may underestimate the data access because the skill is framed around scheduling and free/busy checks.

Mitigation: Disclose before deployment that the skill can expose employee directory data and detailed calendar metadata, not only open meeting times.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/artisong/skills/ms-graph-calendar)
- [Microsoft Graph API](https://graph.microsoft.com)
- [Microsoft Graph OAuth scope](https://graph.microsoft.com/.default)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON snippets emitted by helper scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include employee email resolution, calendar free/busy summaries, meeting-time suggestions, setup guidance, and Graph API error handling.]

## Skill Version(s):

1.0.2 (source: server release metadata; artifact frontmatter states 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
