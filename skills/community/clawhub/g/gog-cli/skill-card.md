## Description:

Google Workspace CLI for Gmail, Calendar, Drive, Contacts, Sheets, and Docs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[saisake](https://clawhub.ai/user/saisake)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and workspace operators use this skill to invoke gog commands for Gmail, Calendar, Drive, Contacts, Sheets, and Docs workflows after OAuth setup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad OAuth-backed Google Workspace access can expose or modify mail, calendar, drive, contacts, sheets, and docs data.

Mitigation: Install only from trusted sources, use the minimum OAuth services needed, and verify the active account before running commands.

Risk: Mail sends, calendar changes, and Sheets clear or update operations can make irreversible workspace changes.

Mitigation: Require confirmation for write actions and verify Gmail message IDs, calendar targets, Sheet IDs, and ranges before execution.

Risk: The Homebrew install source is third-party and not pinned in the release evidence.

Mitigation: Review the Homebrew tap and installed gog binary before using the skill in trusted environments.

## Reference(s):

- [gog homepage](https://gogcli.sh)
- [ClawHub skill page](https://clawhub.ai/saisake/skills/gog-cli)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Markdown, JSON]

**Output Format:** [Markdown with inline shell commands and JSON-oriented CLI output guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the gog CLI, Google Workspace OAuth credentials, and account-specific confirmation for sensitive write actions.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
