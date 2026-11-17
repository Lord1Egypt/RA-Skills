## Description:

帮助用户盘点公司或高校的专利资产，汇总法律状态与技术分布、标记临近到期的专利，并导出资产清单。

This skill is ready for commercial/non-commercial use.

## Publisher:

[ip930](https://clawhub.ai/user/ip930)

### License/Terms of Use:

MIT-0

## Use Case:

企业、高校及其顾问可用此技能进行年度专利盘点、资产管理或准备高新技术企业认定材料。用户提供单位名称和盘点范围后，技能生成专利状态与类型分布摘要，以及可用电子表格打开的专利资产清单。

### Deployment Geography for Use:

Global (China, United States, Europe, Japan, Korea, and WIPO coverage)

## Known Risks and Mitigations:

Risk: Credential handling and cache-path containment warrant review before using a paid key.

Mitigation: Check credential destinations and cache-path containment, supply credentials through protected environment settings rather than chat, and set a spending limit.

Risk: Confidential invention details may be sensitive when submitted to an external patent service.

Mitigation: Submit confidential invention details only with approval.

Risk: Calculated patent expiry dates may differ from current official legal records.

Mitigation: Verify expiry dates and legal status against the official patent register.

## Reference(s):

- [PatentMax skill page](https://clawhub.ai/ip930/skills/patent-portfolio-audit)
- [PatentMax](https://ip930.com)
- [PatentMax API](https://api.ip930.com)
- [API Reference](references/api-reference.md)
- [Search Workflow](references/search-workflow.md)
- [Query Syntax](references/query-syntax.md)
- [Known Pitfalls](references/pitfalls.md)

## Skill Output:

**Output Type(s):** [Text, CSV files]

**Output Format:** [Chinese-language summary and UTF-8 BOM CSV patent asset list]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Expiry years are estimates; verify them against official registers. Patent-name normalization is not performed, and recently filed applications may not yet be published.]

## Skill Version(s):

1.0.3 (source: SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
