## Description:

Operate FileBrowser via REST API: authenticate, list, upload, download, share, and manage resources or users within a configured scope, including workflows for scanning and organizing order files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kami1983](https://clawhub.ai/user/kami1983)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to automate FileBrowser REST API tasks, manage scoped file operations, create share links, and organize order-related files while preserving clear user approval points for sensitive actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bulk organization workflows can move or delete files while recreating them in a target path.

Mitigation: Preview the planned changes and require explicit approval before organizing, overwriting, sharing, or deleting files.

Risk: Examples or API calls that omit the configured scope can operate outside the intended FileBrowser directory.

Mitigation: Use a FileBrowser account restricted server-side to the intended directory, set a narrow scope, and apply that scope to every file operation.

Risk: Credentials, tokens, or local configuration files could be exposed through scripts, logs, uploads, or shared links.

Mitigation: Keep credentials in local configuration or environment variables, do not upload credential files, and avoid logging passwords or tokens.

Risk: Admin-level FileBrowser accounts expand the impact of user-management or file-operation mistakes.

Mitigation: Avoid admin credentials unless user-management tasks are required, and prefer least-privilege accounts for routine file operations.

## Reference(s):

- [FileBrowser API reference](artifact/reference.md)
- [ClawHub skill page](https://clawhub.ai/kami1983/skills/kam-filebrowser-operator)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with HTTP examples, JSON snippets, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include file-operation plans, numbered file selections, download or share-link guidance, and summaries of files that could not be organized.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
