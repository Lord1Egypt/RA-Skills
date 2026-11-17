## Description:

Google Workspace CLI for Gmail, Calendar, Drive, Contacts, Sheets, and Docs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[12357851](https://clawhub.ai/user/12357851)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to get concise setup notes and command examples for using the gog CLI with Gmail, Calendar, Drive, Contacts, Sheets, and Docs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The gog CLI can request broad Google Workspace OAuth access across Gmail, Calendar, Drive, Contacts, Sheets, and Docs.

Mitigation: Install only if the external gog CLI is trusted, authorize only the services needed, and review OAuth scopes before granting access.

Risk: Some example commands can send email, change calendar data, or edit Sheets content.

Mitigation: Confirm mutating commands before execution and use scripted JSON output with noninteractive flags only after reviewing the command intent.

## Reference(s):

- [gog CLI homepage](https://gogcli.sh)
- [ClawHub skill page](https://clawhub.ai/12357851/skills/gog-local-backup)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands include read and write examples for Google Workspace services and should be reviewed before execution.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
