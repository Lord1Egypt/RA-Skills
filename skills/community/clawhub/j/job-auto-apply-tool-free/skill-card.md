## Description:

轻量级求职自动化工具，支持多平台职位搜索与申请提交，自动生成求职信，适合个人求职者提升效率。

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Personal job seekers use this skill to search supported job platforms, compare roles against a candidate profile, generate cover letters, and prepare applications with dry-run and confirmation steps before submission.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can prepare or submit job applications to external platforms using personal profile and resume data.

Mitigation: Start in dry-run mode, require confirmation for every application, and provide resume, profile, or platform credentials only when comfortable with external submission.

Risk: Server security evidence reports unsafe defaults and unclear scope for sending personal applications.

Mitigation: Limit use to explicit job-search tasks, cap application volume, review generated cover letters and matches before submission, and avoid sharing platform tokens unless required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/job-auto-apply-tool-free)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include dry-run application plans, profile configuration examples, platform credential setup guidance, and confirmation-oriented application steps.]

## Skill Version(s):

1.0.3 (source: server release metadata; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
