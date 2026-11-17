## Description:

产业园招商短视频营销专家：AI生成脚本视频、多平台投放方案、客户意向识别留资、线索沉淀腾讯文档。

This skill is ready for commercial/non-commercial use.

## Publisher:

[perrykono-debug](https://clawhub.ai/user/perrykono-debug)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing and leasing staff for industrial parks, office buildings, factories, commercial complexes, urban renewal projects, and industrial communities use this skill to plan short-form promotional videos, draft scripts and publishing materials, review performance data, classify inbound customer intent, and prepare lead capture into an approved Tencent Docs sheet.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Customer phone numbers and messages may be appended to a fixed external Tencent Docs spreadsheet.

Mitigation: Use only an organization-approved sheet, replace hard-coded sheet identifiers with protected deployment configuration, and require confirmation before the first PII write.

Risk: Marketing claims about project details, policies, area, or price may be inaccurate if source data is missing or stale.

Mitigation: Verify project and policy facts through the approved knowledge source before generation and mark missing information as pending rather than inventing details.

Risk: Generated videos, ad plans, customer replies, or budget actions could be published or executed without appropriate review.

Mitigation: Keep publishing, ad spend, targeting, and customer replies under explicit human confirmation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/perrykono-debug/skills/industrial-promo-video)
- [Tencent Docs lead sheet](https://docs.qq.com/sheet/DTHhPaFBHSEV2VGNS)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown with structured scripts, shot lists, publishing materials, analysis, and lead-capture guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include customer intent classifications and Tencent Docs lead-table rows for human-approved follow-up.]

## Skill Version(s):

1.1.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
