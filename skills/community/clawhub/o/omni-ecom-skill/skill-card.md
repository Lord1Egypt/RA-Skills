## Description:

全域电商经营专家团 v2.0.3 用于分析用户授权的电商导出报表，完成店铺诊断、经营周期报告、大促复盘及投流利润分析，并交付经独立复核的图表 PDF。

This skill is ready for commercial/non-commercial use.

## Publisher:

[gzbarry1980-bot](https://clawhub.ai/user/gzbarry1980-bot)

### License/Terms of Use:

MIT-0

## Use Case:

电商经营者和分析人员使用授权导出的店铺报表，诊断业绩、核对指标与来源、规划行动，并生成经过专家复核的经营报告。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive customer information may appear in exported reports or local report files.

Mitigation: Limit access to explicitly authorized exports and protect the locally generated reports and evidence.

Risk: Mistaking report guidance for permission to change a store or access its backend.

Mitigation: Do not supply platform credentials or authorize backend changes without a separately reviewed integration and scoped approval.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/gzbarry1980-bot/skills/omni-ecom-skill)
- [ClawHub distribution and host boundaries](artifact/references/clawhub-distribution.md)
- [Host runtime protocol](artifact/references/runtime-v2.md)
- [Metric contract](artifact/skills/ecom-diagnosis-core/references/metric-contract.md)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Markdown, PDF, JSON]

**Output Format:** [Markdown analysis and charted PDF reports with local JSON evidence]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes traceable calculations and independent review receipts; platform actions are not enabled.]

## Skill Version(s):

2.0.3 (source: ClawHub release metadata, SKILL.md and version-info.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
