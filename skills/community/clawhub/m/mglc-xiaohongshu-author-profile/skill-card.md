## Description:

通过小红书作者主页或作者 ID 查看公开档案，包括简介、粉丝、关注、获赞与收藏、作品数等实际返回字段。适合查询单个博主的当前公开资料。

This skill is ready for commercial/non-commercial use.

## Publisher:

[dunkong](https://clawhub.ai/user/dunkong)

### License/Terms of Use:

MIT-0

## Use Case:

小红书运营人员、研究者或内容团队可用它查询单个作者的当前公开资料，并保留证据、记录接口费用，按需导出结果与报告。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review says reported capabilities extend beyond the single-author profile lookup described, and its local-reference coverage is partial.

Mitigation: Review the requested scope and query plan before running the skill, and confirm that its broader research and reporting features fit the task.

Risk: Live API queries require a customer key and may incur service charges.

Mitigation: Keep the key in the local environment, estimate the maximum API cost, and run only within the user's approved scope and budget.

## Reference(s):

- [ClawHub release](https://clawhub.ai/dunkong/skills/mglc-xiaohongshu-author-profile)
- [Usage guide](references/usage.md)
- [Analysis and evidence format](references/analysis.md)
- [Example query plan](references/example-plan.json)
- [API service](https://api.we-media.cn)

## Skill Output:

**Output Type(s):** [Structured data, Text, Markdown, CSV, HTML, Excel spreadsheet]

**Output Format:** [JSON data and optional Markdown, HTML, CSV, or Excel reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [A current public-profile snapshot; returned fields may vary. Excel export requires optional openpyxl. API requests are billed by the service.]

## Skill Version(s):

1.0.0 (source: skill metadata and server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
