## Description:

笔记创建与管理的规范指南。当需要创建新笔记、管理笔记目录时使用此 skill。包含：笔记层级结构、语言规范、命名规则、通用模板。

This skill is ready for commercial/non-commercial use.

## Publisher:

[tino-chen](https://clawhub.ai/user/tino-chen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, technical writers, and documentation maintainers use this skill to create and organize Chinese-language notes with consistent folder hierarchy, metadata, naming, index pages, and sidebar entries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated notes and sidebar changes could be committed or pushed to the wrong GitHub repository or branch.

Mitigation: Review generated notes and sidebar edits, then confirm the target repository and branch before allowing commit or push actions.

Risk: The skill follows a Chinese-language content convention that may not match every documentation site.

Mitigation: Confirm the target site's language convention before applying the generated note template and sidebar labels.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tino-chen/skills/note-taking)
- [Note management guide](https://tino-chen.github.io/notes/workflows/auto-note-system.html)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown notes, frontmatter, directory/index guidance, and sidebar configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese note content convention with English kebab-case directory and file names]

## Skill Version(s):

1.2.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
