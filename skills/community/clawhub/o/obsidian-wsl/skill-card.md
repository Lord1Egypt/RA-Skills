## Description:

通过 notesmd-cli 操作 Obsidian 知识库 — 搜索、创建、编辑、移动、删除笔记及管理 frontmatter，无需 Obsidian 运行。

This skill is ready for commercial/non-commercial use.

## Publisher:

[kxindot](https://clawhub.ai/user/kxindot)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and knowledge workers use this skill to operate Obsidian vaults from Linux, WSL, or headless terminal environments through notesmd-cli. It helps agents search, read, create, edit, move, delete, and manage frontmatter in Markdown notes without requiring Obsidian to be running.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on an unpinned third-party Homebrew tap for notesmd-cli.

Mitigation: Install only when the notesmd-cli Homebrew tap is trusted and review the installed CLI before using it with sensitive vaults.

Risk: Overwrite, move, frontmatter delete, and note delete commands can change or remove vault content.

Mitigation: Review destructive commands before execution and keep backups or version control for important vaults.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kxindot/skills/obsidian-wsl)
- [kxindot publisher profile](https://clawhub.ai/user/kxindot)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires notesmd-cli and access to the user's configured Obsidian vaults.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
