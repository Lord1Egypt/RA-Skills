## Description:

Google Sheets Secure Management helps agents create, read, write, append, copy, share, rename, delete, and manage tabs for Google Sheets through the porteden CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[porteden](https://clawhub.ai/user/porteden)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and AI agents use this skill to manage Google Sheets data, spreadsheet files, tabs, and permissions from natural-language workflows backed by porteden CLI commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on the third-party porteden CLI and credentials with Google Sheets or Drive access.

Mitigation: Install only from trusted porteden sources, use a dedicated Google account or profile when practical, and keep PE_API_KEY narrowly scoped.

Risk: Spreadsheet sharing and delete operations can expose or remove user data.

Mitigation: Manually confirm share and delete operations before execution, and prefer restricted sharing scopes.

Risk: Broad Drive scopes can grant access beyond a single spreadsheet workflow.

Mitigation: Avoid broad Drive scopes unless required for the task, and verify token access information before sensitive operations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/porteden/skills/google-sheets-skill)
- [PortEden publisher profile](https://clawhub.ai/user/porteden)
- [PortEden homepage](https://porteden.com)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include compact JSON-oriented command flags for AI-friendly spreadsheet responses.]

## Skill Version(s):

1.0.8 (source: evidence.json release.version and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
