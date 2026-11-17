## Description:

将亚马逊买家评论中的抱怨整理为按影响人数与严重程度排序的产品改进建议。

This skill is ready for commercial/non-commercial use.

## Publisher:

[funewa](https://clawhub.ai/user/funewa)

### License/Terms of Use:

MIT-0

## Use Case:

面向亚马逊卖家和产品运营人员，帮助他们从商品评论中识别质量问题，并为下一轮产品开发确定改模具、材料、包装或说明书等改进优先级。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Paid analysis or collection may spend service credits without fresh approval because the release's quote-only and confirmation guidance is unreliable.

Mitigation: Set account confirmation to ask every time, use quotes for estimates, and require fresh approval before each paid action. Use a corrected release that enforces these boundaries.

Risk: Recurring review collection can incur ongoing credit charges.

Mitigation: Require separate approval for recurring collection and confirm the schedule and current quoted cost before enabling it.

## Reference(s):

- [ARI 产品运营工作台](https://ari.funewa.com/zh/operations)
- [ARI 监控中心](https://ari.funewa.com/zh/monitor)
- [ARI 报告中心](https://ari.funewa.com/zh/reports)
- [API 参考](references/reference.md)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Markdown, Files]

**Output Format:** [自然语言分析与优先级建议，通常以 Markdown 呈现；按需导出评论 CSV 或报告文件。]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [结论取决于可用评论样本与时间范围；不要将样本频次解释为市场搜索量或销量。]

## Skill Version(s):

1.5.3 (source: server-resolved release, CHANGELOG)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
