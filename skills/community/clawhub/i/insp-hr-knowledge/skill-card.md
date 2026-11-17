## Description:

INSP 公司 HR 知识库查询技能，帮助员工查询入职、考勤、加班、报销、离职、财务 SOP、系统使用和公司文化等内部政策与流程。

This skill is ready for commercial/non-commercial use.

## Publisher:

[frank-git1](https://clawhub.ai/user/frank-git1)

### License/Terms of Use:

MIT-0

## Use Case:

Employees use this skill to quickly answer questions about INSP internal HR policies, onboarding, attendance, overtime, reimbursement, offboarding, finance procedures, system usage, and company culture.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill embeds a corporate Wi-Fi password in published knowledge content.

Mitigation: Remove the password, rotate the credential, and provide network access details through an authenticated IT channel.

Risk: The skill combines HR, finance, procurement, and system procedures that may be intended for different employee roles.

Mitigation: Split sensitive SOPs into narrower role-scoped skills or add access controls before publishing.

Risk: The skill contains internal company policies and procedures that may be inappropriate for external audiences.

Mitigation: Review distribution scope and confirm that the package is only available to authorized users.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/frank-git1/skills/insp-hr-knowledge)
- [Source document](https://i1p42lnph7o.feishu.cn/docx/X1SxdSv7kohxdXxzTyJcXOFgneh)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown responses with policy summaries, lists, and tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Answers are based on static internal HR knowledge embedded in the skill.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
