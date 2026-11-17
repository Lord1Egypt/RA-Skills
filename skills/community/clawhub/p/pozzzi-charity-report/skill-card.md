## Description:

噗滋（pozzzi）慈善 - 帮助中小型 NGO 自动生成年度工作报告、项目结项报告和财务决算报告草稿，确保法定章节不遗漏，输出符合民政部和资助方格式要求。

This skill is ready for commercial/non-commercial use.

## Publisher:

[aikawabigsky309](https://clawhub.ai/user/aikawabigsky309)

### License/Terms of Use:

MIT-0

## Use Case:

External NGO staff and operators use this skill to draft Chinese annual work reports, project closeout reports, and financial closeout reports from structured organization, program, and finance data. The generated reports are drafts for human legal, financial, and management review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive beneficiary, contact, health, disability, child-related, account, or address details may still be sent to model providers despite claimed privacy controls.

Mitigation: Use anonymized inputs only, verify the configured model gateway blocks PII before deployment, and require human legal and financial review before using generated reports.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aikawabigsky309/skills/pozzzi-charity-report)
- [Ministry of Civil Affairs template source](https://www.mca.gov.cn/article/yw/hjzcbz/2017/201710/20171000006382.shtml)
- [Tencent Charity helper reference](https://www.qq.com/charity/helper/index.htm)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown report drafts with AI-use and disclaimer text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports full report generation and single-section regeneration; token limits vary by report type.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
