## Description:

Google Workspace CLI for Gmail, Calendar, Drive, Contacts, Sheets, and Docs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaomaju-888](https://clawhub.ai/user/xiaomaju-888)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to work with Google Workspace services through the gog CLI, including mail, calendar, files, contacts, Sheets, and Docs tasks after OAuth setup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to install an unpinned third-party CLI.

Mitigation: Review the gogcli source and Homebrew formula before installing, and pin or otherwise control the installed package in managed environments.

Risk: OAuth setup can grant broad Google Workspace access, including sensitive read and write operations.

Mitigation: Authorize only the Google services needed for the task and revoke the OAuth grant when the tool is no longer needed.

Risk: Some examples send email, create calendar events, or modify Sheets data.

Mitigation: Confirm state-changing commands before execution and prefer --json plus --no-input for scripted workflows.

## Reference(s):

- [Gog CLI homepage](https://gogcli.sh)
- [Gog Xiaoshu on ClawHub](https://clawhub.ai/xiaomaju-888/skills/gog-xiaoshu)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes setup notes and examples; gog commands may emit JSON when run with --json.]

## Skill Version(s):

1.0.0 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
