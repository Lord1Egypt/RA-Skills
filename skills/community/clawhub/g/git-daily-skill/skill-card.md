## Description:

今日 Git 提交日报助手，自动扫描当天含次日凌晨 6 点前的多仓库 commit 记录并生成结构化日报。

This skill is ready for commercial/non-commercial use.

## Publisher:

[kenneychen](https://clawhub.ai/user/kenneychen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill at the end of a workday to scan one or more local Git repositories and summarize their own commits in a daily report. It supports current-day and historical date review across a 06:00 to next-day 05:59 work window.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can scan Git repositories under the current or specified root and expose commit metadata to the assistant.

Mitigation: Run it with an explicit narrow --root path and avoid directories that contain unrelated or confidential repositories.

Risk: Commit messages and author metadata may include sensitive project context even though the skill does not write files, persist data, or send data out.

Mitigation: Review the selected scan root and generated report before sharing the output outside the intended workspace.

## Reference(s):

- [GitPulse README](README.md)
- [ClawHub Skill Page](https://clawhub.ai/kenneychen/skills/git-daily-skill)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown or plain text daily report, with JSON available from the bundled script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The report includes per-repository commit counts, commit details, activity statistics, and a short Chinese commentary.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
