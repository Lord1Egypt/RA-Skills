## Description: <br>
模型消耗统计技能，用于统计和展示不同会话、不同模型的 token 使用量、成本统计和消耗报告，通过飞书消息卡片进行可视化展示。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[luxiang79](https://clawhub.ai/user/luxiang79) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and external ClawHub users use this skill to summarize model token usage, estimate costs, compare consumption by model or session, and format the results as Feishu message cards or reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Usage summaries sent to Feishu may expose session IDs or detailed per-session activity in shared channels. <br>
Mitigation: Prefer aggregate totals for shared channels, redact session IDs, and export detailed per-session reports only when the user explicitly needs them. <br>
Risk: Cost calculations rely on model pricing examples and may become inaccurate when provider pricing changes. <br>
Mitigation: Treat cost output as an estimate and confirm current model pricing before using the report for billing or budget decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/luxiang79/model-usage-stats) <br>
- [Publisher profile](https://clawhub.ai/user/luxiang79) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown reports and Feishu message-card content with tables, summaries, and cost calculations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include session-level usage summaries, model-level breakdowns, cost estimates, and exportable report text.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
