## Description:

自动获取上周的 Git 提交记录，并生成简洁的 3 点周报总结。适用于需要快速整理个人工作进展的场景。

This skill is ready for commercial/non-commercial use.

## Publisher:

[yinwuzhe](https://clawhub.ai/user/yinwuzhe)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to review their own recent repository activity and prepare a concise weekly progress report from the past seven days of non-merge commits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Commit subjects enter the agent's context and may contain confidential information.

Mitigation: Run the skill only in the repository intended for the report, and consider the confidentiality of its commit subjects.

Risk: Commits authored under a different Git identity may be omitted from the report.

Mitigation: Check that the configured Git author name matches the commits you want included.

## Reference(s):


## Skill Output:

**Output Type(s):** [Markdown, Text]

**Output Format:** [Markdown with three concise work highlights]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Summarizes non-merge Git commits from the preceding seven days into three key points.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
