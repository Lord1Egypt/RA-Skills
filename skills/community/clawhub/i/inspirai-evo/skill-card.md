## Description:

技能自我进化 - 检测流程问题信号（重复试错、流程中断、代码翻动），生成分析报告，引导改进。

This skill is ready for commercial/non-commercial use.

## Publisher:

[alexxxiong](https://clawhub.ai/user/alexxxiong)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to detect repeated workflow problems such as retry loops, interrupted work, and git churn, then generate concise improvement reports and pending follow-up items.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may persist workflow context, project names, timestamps, patterns, and pending improvement details in project-local files and under the user's home directory.

Mitigation: Review generated files before sharing or committing them, keep sensitive reports out of version control unless intended, and remove local or global stats when retention is not desired.

Risk: The --continue flow can turn pending improvement items into proposed file changes.

Mitigation: Use --continue only after reviewing the pending items and confirm each proposed change before applying it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alexxxiong/skills/inspirai-evo)
- [Publisher profile](https://clawhub.ai/user/alexxxiong)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown reports with shell command snippets and JSON state updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create project-local reports and state files plus cross-project local statistics.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
