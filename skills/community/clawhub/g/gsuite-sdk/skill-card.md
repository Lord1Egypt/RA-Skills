## Description:

Work with Gmail, Google Calendar, Drive, Sheets, Tasks and Contacts, and read Search Console, Google Analytics 4 and Tag Manager, through the gsuite-sdk Python library and its gsuite CLI, with JSON output for agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pabloalaniz](https://clawhub.ai/user/pabloalaniz)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents can use the skill to access Google Workspace services and retrieve search, traffic, and tag data. It can also create or modify email, calendar events, files, spreadsheets, tasks, and contacts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release security assessment flags an unpinned MCP package and credential export that may leave a local token file exposed; scanner coverage is partial.

Mitigation: Review and fix the MCP package version before installing. Protect exported token files with restrictive permissions, keep them out of shared or backed-up locations, remove them when no longer needed, and account for the incomplete scan coverage.

Risk: Email, calendar, Drive, and other write operations can affect external accounts or change user data.

Mitigation: Confirm with the user before sending email, inviting attendees, sharing files, or deleting data, as directed by the skill documentation.

## Reference(s):

- [gsuite-sdk documentation](https://pabloalaniz.github.io/google-suite/)
- [Release notes for 0.14.0](https://github.com/PabloAlaniz/google-suite/releases/tag/v0.14.0)

## Skill Output:

**Output Type(s):** [JSON data, Files, API results]

**Output Format:** [Structured JSON or Python API results; files may be downloaded or uploaded.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions may send email, invite attendees, share files, or change or delete data; confirm with the user before these actions.]

## Skill Version(s):

0.14.0 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
