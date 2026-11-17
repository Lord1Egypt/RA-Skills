## Description:

Google Docs Secure Management. Use when the user wants to create, read, or edit Google Docs content; or manage sharing, permissions, renames, and deletes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[porteden](https://clawhub.ai/user/porteden)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to operate Google Docs through the PortEden CLI, including document creation, reads, edits, downloads, sharing, permission checks, renames, and trash operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs and uses an unpinned third-party CLI for access to a high-impact document account.

Mitigation: Review before installing and prefer a pinned or verified PortEden release instead of an unverified tap or @latest install.

Risk: Direct token login can expose credentials through shell history or process visibility.

Mitigation: Prefer browser login, or use the narrowest possible token and Drive scopes when a token is required.

Risk: Sharing and trash operations can expose or remove Google Docs files.

Mitigation: Confirm sharing, permission, and delete commands manually before execution.

## Reference(s):

- [PortEden](https://porteden.com)
- [ClawHub Google Docs Skill](https://clawhub.ai/porteden/skills/google-docs-cli)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include compact JSON-oriented command flags, provider-prefixed Google file IDs, and credential or sharing cautions.]

## Skill Version(s):

1.0.8 (source: server release and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
