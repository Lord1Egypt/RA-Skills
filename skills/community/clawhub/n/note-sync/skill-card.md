## Description:

Append notes to local Markdown files via MCP append_note when the user asks to save ideas, reminders, or journal entries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lgwventrue](https://clawhub.ai/user/lgwventrue)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to save chat content as local Markdown notes through the append_note MCP tool. It is suited for reminders, journal entries, and named note files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires users to run an external MCP executable that the security evidence describes as unaudited.

Mitigation: Review and trust the MCP repository before installing, and prefer a fixed, verified release or commit with a checksum.

Risk: Saved content is written to local files under the configured notes directory.

Mitigation: Avoid saving sensitive content unless the local notes directory and machine access controls are appropriate for that data.

Risk: Setup depends on NOTE_SYNC_REPO and mcp.servers.note-sync being configured correctly.

Mitigation: Confirm the environment variable, MCP command, and expected notes path before relying on the skill.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/lgwventrue/skills/note-sync)
- [Setup Guide](references/setup.md)
- [append_note Tool Reference](references/tool-reference.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown notes and plain-text confirmations, with setup guidance in Markdown and shell or PowerShell snippets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes note content to local Markdown files under the configured notes directory.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter says 1.0.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
