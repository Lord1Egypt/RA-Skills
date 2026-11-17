## Description:

文件快速扫描通过生成精简项目索引，帮助 AI 在不打开每个文件的情况下判断内容并减少重复读取带来的 token 消耗。

This skill is ready for commercial/non-commercial use.

## Publisher:

[adchina2025](https://clawhub.ai/user/adchina2025)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to scan local project directories and produce compact Markdown indexes that help decide which files need to be read. It can also summarize reimbursement directories and optionally flag recent Downloads files when that scan is explicitly requested.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can scan local project files and write an index that future agent sessions may rely on, including text from untrusted files.

Mitigation: Use it only on projects you are comfortable indexing locally and inspect the generated .anatomy.md before relying on it for agent context.

Risk: Startup auto-refresh can rescan stale indexes in repositories that may not be trusted.

Mitigation: Avoid startup auto-refresh on untrusted repositories; run manual scans with explicit excludes, depth limits, and output paths when review is needed.

Risk: The optional Downloads scan can include recent personal Downloads metadata in the generated index.

Mitigation: Do not use --scan-downloads unless recent personal Downloads metadata is intended to be included.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/adchina2025/skills/project-anatomy)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration]

**Output Format:** [Markdown index files and terminal text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes .anatomy.md by default and may write a companion .cache.json for incremental scans; optional Downloads metadata is included only when --scan-downloads is used.]

## Skill Version(s):

0.1.4 (source: server release metadata and artifact/skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
