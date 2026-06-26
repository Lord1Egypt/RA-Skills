## Description: <br>
噗滋（pozzzi）慈善 - 帮助中小型 NGO 自动生成年度工作报告、项目结项报告和财务决算报告草稿，确保法定章节不遗漏，输出符合民政部和资助方格式要求。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aikawabigsky309](https://clawhub.ai/user/aikawabigsky309) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External NGO staff and operators use this skill to draft Chinese annual work reports, project closeout reports, and financial final reports from structured organization, project, and finance data. It is intended to produce editable drafts that preserve required sections and must be reviewed before submission. <br>

### Deployment Geography for Use: <br>
China <br>

## Known Risks and Mitigations: <br>
Risk: Legal or financial report drafts may contain incorrect, incomplete, or unsuitable content for formal submission. <br>
Mitigation: Manually review all legal and financial report content before submission and verify figures against source records. <br>
Risk: Identifiable beneficiary stories or data about children under 14 could create privacy and compliance exposure. <br>
Mitigation: Avoid entering identifiable beneficiary stories or data about children under 14; use anonymized or aggregated descriptions before model processing. <br>
Risk: The skill relies on external shared components for model routing, storage, and disclaimer injection. <br>
Mitigation: Confirm the model gateway, storage adapter, and disclaimer injector used in the deployment, and use scoped provider API keys. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aikawabigsky309/pozzzi-charity-report) <br>
- [Ministry of Civil Affairs annual report reference](https://www.mca.gov.cn/article/yw/hjzcbz/2017/201710/20171000006382.shtml) <br>
- [Tencent Charity helper reference](https://www.qq.com/charity/helper/index.htm) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown report draft with AI-assisted-generation and disclaimer text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports full report generation and single-section regeneration for annual work, project closeout, and financial final reports.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
