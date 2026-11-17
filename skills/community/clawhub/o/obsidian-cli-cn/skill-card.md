## Description:

Obsidian笔记命令行工具，支持笔记搜索、批量处理、统计分析、导出转换、标签管理等功能，直接操作本地Obsidian知识库。

This skill is ready for commercial/non-commercial use.

## Publisher:

[paudyyin](https://clawhub.ai/user/paudyyin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and knowledge workers use this skill to operate a local Obsidian vault from the command line for note search, vault statistics, bulk content changes, export, tag workflows, and link checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bulk replace operations can rewrite many local notes without built-in safeguards.

Mitigation: Use the skill only on a backed-up or version-controlled Obsidian vault, and review the target vault and replacement pattern before running bulk changes.

Risk: Search and replace patterns are treated as regular expressions, which can match more text than intended.

Mitigation: Escape regular expression characters when literal matching is intended and test patterns on a small vault or limited query before applying replacements broadly.

Risk: The vault may contain important personal or work notes.

Mitigation: Run commands only against the intended local vault path and avoid running bulk operations on untrusted or unfamiliar vaults.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/paudyyin/skills/obsidian-cli-cn)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, files, guidance]

**Output Format:** [Markdown guidance with inline shell commands and command output summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read local Markdown notes, rewrite note contents, and export files from an Obsidian vault.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
