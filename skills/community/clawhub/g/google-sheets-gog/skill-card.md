## Description:

Use this skill when you need to create, inspect, update, append to, or reorganize Google Sheets from a locally installed `gog` CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kvarts](https://clawhub.ai/user/kvarts)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to operate Google Sheets through the local `gog` CLI for spreadsheet reads, appends, updates, creation, tab management, named ranges, exports, and carefully confirmed broad changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a password-like configuration value before it can load.

Mitigation: Avoid storing real passwords or reusable secrets in ordinary config; prefer OAuth-only setup, environment references, or a secret manager.

Risk: Spreadsheet writes can clear, overwrite, restructure, or delete user data when commands are broad or destructive.

Mitigation: Confirm the spreadsheet ID, tab or named range, exact range, and operation before destructive or broad writes.

Risk: Commands may use broader Google account access than needed for a read-only task.

Mitigation: Use Sheets-scoped commands and prefer read-only authorization for inspection sessions.

## Reference(s):

- [gog Sheets Reference](references/gog-sheets.md)
- [gogcli Homepage](https://github.com/steipete/gogcli)
- [gogcli README](https://github.com/steipete/gogcli/blob/main/README.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Markdown, Code]

**Output Format:** [Markdown guidance with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands are intended to be scoped to explicit spreadsheet IDs, tab names, and A1 ranges, with confirmation before destructive or broad writes.]

## Skill Version(s):

1.1.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
