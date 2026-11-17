## Description:

Google Workspace CLI for Gmail, Calendar, Drive, Contacts, Sheets, and Docs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[blueworldmarketing](https://clawhub.ai/user/blueworldmarketing)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to configure and run the gog CLI for Google Workspace tasks across Gmail, Calendar, Drive, Contacts, Sheets, and Docs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a third-party Homebrew install for gog.

Mitigation: Review the Homebrew tap and gogcli publisher before installing, and do not run the CLI as root.

Risk: The CLI can request broad Google Workspace account access.

Mitigation: Authorize only the Google services needed for the task.

Risk: Commands can send mail, create calendar events, or modify and clear Sheets data.

Mitigation: Review data-changing commands before execution, especially mail, calendar, and Sheets operations.

## Reference(s):

- [gog homepage](https://gogcli.sh)
- [ClawHub skill page](https://clawhub.ai/blueworldmarketing/skills/gog-bwm)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes OAuth setup guidance and optional JSON-output CLI examples for scripting.]

## Skill Version(s):

1.0.0 (source: release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
