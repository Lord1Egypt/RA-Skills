## Description:

Google Workspace CLI for Gmail, Calendar, Drive, Contacts, Sheets, and Docs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[litiao1224](https://clawhub.ai/user/litiao1224)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and developers use this skill to prepare and run gog CLI commands for Gmail, Calendar, Drive, Contacts, Sheets, and Docs workflows after OAuth is configured.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide commands that send mail, create calendar items, or change Sheets data.

Mitigation: Review high-impact commands before execution, especially mail sending, calendar creation, Sheets updates, and sheets clear.

Risk: The gog CLI requires OAuth access to Google Workspace services including mail, calendar, drive, contacts, docs, and spreadsheets.

Mitigation: Install only from trusted gog Homebrew sources and enable only the Google Workspace scopes needed for the task.

## Reference(s):

- [gog CLI homepage](https://gogcli.sh)
- [ClawHub Gog Litiao skill page](https://clawhub.ai/litiao1224/skills/gog-litiao)
- [ClawHub litiao1224 publisher profile](https://clawhub.ai/user/litiao1224)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands may access Google Workspace data when executed with configured OAuth credentials.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
