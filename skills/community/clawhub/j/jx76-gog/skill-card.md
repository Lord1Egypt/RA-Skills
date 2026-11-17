## Description:

Google Workspace CLI for Gmail, Calendar, Drive, Contacts, Sheets, and Docs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jx-76](https://clawhub.ai/user/jx-76)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external users, and developers use this skill to operate the gog CLI for Gmail, Calendar, Drive, Contacts, Sheets, and Docs workflows after OAuth setup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The gog CLI uses sensitive OAuth access to Google Workspace services.

Mitigation: Install only when the gog CLI and Homebrew tap are trusted, and authorize only the minimum Google services needed.

Risk: Commands can send email, create calendar events, or update, append, and clear spreadsheet data.

Mitigation: Review destructive or externally visible commands before execution and prefer JSON and no-input modes for scripts.

## Reference(s):

- [gog homepage](https://gogcli.sh)
- [ClawHub skill page](https://clawhub.ai/jx-76/skills/jx76-gog)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance may include OAuth setup steps and user-directed gog commands that can read or modify Google Workspace data.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
