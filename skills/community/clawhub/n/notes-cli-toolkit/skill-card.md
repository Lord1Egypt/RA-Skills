## Description:

This skill guides agents through Obsidian vault automation with notesmd-cli, including headless note creation, frontmatter maintenance, daily-note generation, and editor-based workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, knowledge workers, and automation teams use this skill to manage Obsidian vaults as scriptable note collections. It is intended for requested vault tasks such as batch Markdown edits, frontmatter updates, daily-note creation, and CI-assisted note maintenance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence flags broad trigger language and routine bulk file mutations.

Mitigation: Use only for clearly requested Obsidian vault tasks, review dry-run previews before bulk edits or moves, and keep backups or version control enabled.

Risk: The security evidence notes inconsistent API and network claims.

Mitigation: Do not provide API keys, callback URLs, or Git push credentials unless the user specifically intends a networked CI workflow.

Risk: The security verdict is suspicious and recommends review before installation.

Mitigation: Review the skill and its commands before installing or executing it in an agent environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/notes-cli-toolkit)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose or execute bulk Markdown file mutations in an Obsidian vault; use previews, backups, or version control before applying changes.]

## Skill Version(s):

1.0.2 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
