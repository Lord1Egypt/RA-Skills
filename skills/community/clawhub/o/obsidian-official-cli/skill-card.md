## Description:

Work with Obsidian vaults using the official Obsidian CLI (v1.12+). Open, search, create, move, and manage notes from the terminal.

This skill is ready for commercial/non-commercial use.

## Publisher:

[slmoloch](https://clawhub.ai/user/slmoloch)

### License/Terms of Use:

MIT

## Use Case:

Developers, knowledge workers, and agents use this skill to operate a live Obsidian vault from the terminal, including note management, search, tasks, properties, links, plugins, themes, sync, and developer utilities.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can enable an agent to inspect and change a live Obsidian vault.

Mitigation: Use explicit prompts for vault-changing actions and keep backups of important vaults.

Risk: Commands can permanently delete, overwrite, restore, or otherwise alter vault content and Obsidian settings.

Mitigation: Require confirmation before permanent deletion, overwrites, restores, plugin or theme changes, and sync-affecting operations.

Risk: Developer commands can run eval, inspect the DOM, or capture screenshots from the active Obsidian environment.

Mitigation: Require confirmation before eval, screenshots, DOM inspection, CSS inspection, or other developer-tool commands.

## Reference(s):

- [Obsidian Official CLI Documentation](https://help.obsidian.md/cli)
- [OpenClaw Documentation](https://docs.openclaw.ai)
- [ClawHub Skill Page](https://clawhub.ai/slmoloch/skills/obsidian-official-cli)
- [Publisher Profile](https://clawhub.ai/user/slmoloch)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose commands that inspect or modify a live Obsidian vault and its settings.]

## Skill Version(s):

1.0.0 (source: server release evidence and CHANGELOG, released 2026-02-10)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
