## Description:

噗滋（pozzzi）慈善 - 帮助中小型 NGO 自动生成项目申报书草稿，支持腾讯公益99公益日、通用基金会申请和政府购买服务三种格式，内置占位符强制机制防止 AI 编造预算和编号数据。

This skill is ready for commercial/non-commercial use.

## Publisher:

[aikawabigsky309](https://clawhub.ai/user/aikawabigsky309)

### License/Terms of Use:

MIT-0

## Use Case:

External NGO staff and grant writers use this skill to draft Chinese project application materials for foundation funding, Tencent 99 Giving Day, and government service procurement. It helps structure provided organization, project, timeline, budget, and impact data into Markdown application drafts for human review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Draft inputs may contain personal information about staff, volunteers, partners, beneficiaries, or minors, including personal data embedded in narrative or nested fields.

Mitigation: Review inputs before use, remove individual-level details, and only provide data that may be sent to the configured model provider.

Risk: The local validator is not a complete PII blocker.

Mitigation: Treat validation as a support control, not a privacy boundary, and perform human privacy review before generating or submitting drafts.

Risk: Generated application drafts can contain incomplete, incorrect, or placeholder financial and registration details.

Mitigation: Require responsible staff to replace placeholders, verify budgets, confirm identifiers, and review all AI-assisted content before submission.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aikawabigsky309/skills/pozzzi-charity-application)
- [Tencent Gongyi](https://gongyi.qq.com/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown application draft with warnings and generation metadata]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs include AI disclosure text, placeholder substitutions for sensitive identifiers, and warnings when validation or placeholder enforcement detects issues.]

## Skill Version(s):

0.1.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
