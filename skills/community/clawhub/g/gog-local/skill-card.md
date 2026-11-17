## Description:

Google Workspace CLI for Gmail, Calendar, Drive, Contacts, Sheets, and Docs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[czm448](https://clawhub.ai/user/czm448)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to work with Gmail, Calendar, Drive, Contacts, Sheets, and Docs from an agent-assisted command-line workflow after configuring OAuth access.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to install an unpinned third-party Homebrew CLI that will handle broad Google account permissions.

Mitigation: Review the gog Homebrew tap and package provenance before installing, and install only from a trusted release path.

Risk: The CLI can perform mutating Google Workspace actions, including sending mail, creating calendar events, and updating or clearing Sheets data.

Mitigation: Use a dedicated or least-privilege Google account where possible, grant only the Google services needed, and confirm mail, calendar, and Sheets changes before running them.

## Reference(s):

- [Gog CLI homepage](https://gogcli.sh)
- [Gog Local on ClawHub](https://clawhub.ai/czm448/skills/gog-local)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include JSON-oriented command flags such as --json and --no-input for scripting workflows.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
