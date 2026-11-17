## Description:

生成A股个股深度投资报告。当用户要求撰写股票/公司投资报告、个股分析、估值分析时使用。支持批量生成多份报告。报告包含：公司概况、详细业务构成、财务分析与预测、分部估值(SOTP)、投资逻辑、交易计划、多维度深度分析（政策面/基本面/技术面/情绪面/消息面/资金面）、风险提示、总结。用户只需提供公司名称列表即可触发。

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiu-chuan](https://clawhub.ai/user/jiu-chuan)

### License/Terms of Use:

MIT-0

## Use Case:

External users and analysts use this skill to draft Chinese A-share company investment reports from company names, including business analysis, financial forecasts, SOTP valuation, investment logic, trading plans, risk disclosures, and summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can produce concrete trading plans that may be mistaken for personalized financial advice.

Mitigation: Treat generated reports as research drafts only, keep the included disclaimer, and require independent human review before any investment decision.

Risk: Market, company, valuation, and technical-analysis data may be incomplete, stale, or inaccurate.

Mitigation: Verify all financial data, prices, institutional forecasts, and cited market signals against authoritative current sources before relying on the report.

Risk: The skill can save generated reports automatically in the workspace by default.

Mitigation: Run it only in an intended workspace and review generated filenames and files before sharing or committing them.

## Reference(s):

- [Report Template](references/template.md)
- [ClawHub Skill Page](https://clawhub.ai/jiu-chuan/skills/investment-report)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown investment reports saved as .md files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports single-company and batch report generation; reports include financial analysis, valuation, trading-plan sections, risk disclosures, and a disclaimer.]

## Skill Version(s):

0.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
