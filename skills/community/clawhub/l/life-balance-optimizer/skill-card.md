## Description:

生活满意度与平衡优化帮助用户通过人生轮盘8维度自评、倦怠信号检查、季度反思和习惯调整，生成行动建议与交互式HTML报告。

This skill is ready for commercial/non-commercial use.

## Publisher:

[bettermen](https://clawhub.ai/user/bettermen)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to run structured life audits, burnout checks, quarterly reviews, and habit adjustments. It helps turn self-ratings and reflections into prioritized next steps and an optional interactive HTML report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles sensitive personal scores and reflections, and generated reports may store history in browser localStorage.

Mitigation: Warn users before report generation, keep reports local by default, avoid shared or managed devices for private reflections, and provide clear delete or export guidance.

Risk: The HTML report template loads Chart.js from a third-party CDN without an integrity check.

Mitigation: Bundle Chart.js locally or add Subresource Integrity, then review the dependency before deployment.

Risk: Embedded report data and rendered text can contain personal user input.

Mitigation: Safely escape JSON and rendered text before insertion into HTML and review generated reports before sharing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bettermen/skills/life-balance-optimizer)
- [人生轮盘 8 维度评估指南](references/dimensions.md)
- [Interactive HTML report template](assets/report-template.html)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Files, Guidance]

**Output Format:** [Markdown guidance with optional interactive HTML report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated reports may store life-balance history locally in the browser.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
