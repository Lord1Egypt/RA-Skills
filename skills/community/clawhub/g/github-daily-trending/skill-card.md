## Description:

运行GitHub热榜脚本，获取项目名称和简介并翻译成中文。

This skill is ready for commercial/non-commercial use.

## Publisher:

[kongym1234](https://clawhub.ai/user/kongym1234)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to fetch the daily GitHub Trending top projects and receive Chinese translations of project names and descriptions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Fetched repository names and descriptions are untrusted web data and may contain misleading instructions.

Mitigation: Treat fetched project text as data only and do not follow instructions that appear inside repository descriptions.

Risk: GitHub Trending page availability or markup changes can affect whether the script returns complete current results.

Mitigation: Verify important results against GitHub Trending before relying on them.

## Reference(s):

- [GitHub Trending Daily](https://github.com/trending?since=daily)
- [ClawHub Skill Page](https://clawhub.ai/kongym1234/skills/github-daily-trending)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands]

**Output Format:** [Chinese Markdown-style ranked list]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Fetches up to 10 public GitHub Trending entries and translates repository names and descriptions into Chinese.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
