## Description:

Google Workspace CLI for Gmail, Calendar, Drive, Contacts, Sheets, and Docs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sieyer](https://clawhub.ai/user/sieyer)

### License/Terms of Use:


## Use Case:

Developers and workspace operators use this skill to run gog CLI commands for Gmail, Calendar, Drive, Contacts, Sheets, and Docs workflows after OAuth setup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to install an unpinned third-party CLI before use.

Mitigation: Review the gog CLI source and Homebrew formula before installing, and install from a trusted source.

Risk: The skill requires OAuth access to sensitive Google Workspace data across Gmail, Calendar, Drive, Contacts, Sheets, and Docs.

Mitigation: Grant only the Google services needed for the task, use a separate or restricted account where practical, and revoke OAuth tokens if credentials or the CLI may have been exposed.

Risk: OAuth client secrets and tokens can expose workspace data if shared or committed.

Mitigation: Keep client_secret.json and token material out of source control, shared folders, and logs.

## Reference(s):

- [gog homepage](https://gogcli.sh)
- [ClawHub skill page](https://clawhub.ai/sieyer/skills/gog-1-0-0)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The guidance expects the third-party gog binary, OAuth credentials, and optional JSON output flags for scripting.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
