## Description:

Obsidian CLI(专业版) helps agents administer Obsidian vaults through command-line workflows for files, search, templates, plugins, themes, Sync, history restore, developer tools, workspaces, and TUI interaction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, advanced Obsidian users, and teams use this skill to automate knowledge-vault operations such as bulk file maintenance, link audits, template-based note creation, plugin and theme management, Sync history recovery, and plugin debugging.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can propose permanent delete, overwrite, restore, sync pause/resume, plugin install/uninstall, and eval commands that alter an Obsidian vault.

Mitigation: Require explicit approval before these actions and keep vault backups or Sync history available before use.

Risk: The security summary says the skill exposes powerful vault-changing commands without enough built-in guardrails.

Mitigation: Review proposed commands before execution and restrict use to intentional Obsidian vault administration workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/obsidian-cli-tool-pro)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON result examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose commands that change Obsidian vault contents; approvals and backups are recommended before destructive operations.]

## Skill Version(s):

1.0.1 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
