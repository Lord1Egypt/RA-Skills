## Description:

京东黄金ToC智能助手：实时金价查询（京东24h/上金所/伦敦金/7家银行积存金）、持仓收益与诊断、交易记录与条件单、黄金综合分析、贵金属行情与K线、资讯快讯、大V排行、黄金模拟交易（模拟买卖与全自动托管盯盘）。

This skill is ready for commercial/non-commercial use.

## Publisher:

[xuqingyuan0902-dot](https://clawhub.ai/user/xuqingyuan0902-dot)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to query JD Gold and precious-metals prices, read gold-market news and analysis, and review JD account-specific accumulated-gold holdings, returns, trade records, and conditional orders after authorization. It can also guide simulated gold trading and locally scheduled simulated-trading automation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles JD account authorization for account-specific holdings, returns, trade records, and conditional orders.

Mitigation: Install only when the publisher is trusted, grant authorization deliberately, and avoid shared machines or environments where local files or environment variables may be readable by others.

Risk: The skill includes background simulated-trading automation.

Mitigation: Before enabling automation, confirm the schedule, spending limits, token lifetime, and the procedure for stopping and removing the scheduled task.

Risk: The security summary identifies an unsafe self-update path.

Mitigation: Review update behavior before installation and prefer verified release artifacts from the ClawHub skill page.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/xuqingyuan0902-dot/skills/jdgold)
- [Agent Operations](references/agent-ops.md)
- [Safety and Output Rules](references/iron-rules.md)
- [JD Gold OAuth Integration](references/oauth-integration.md)
- [JD Gold Market Search](references/jdjr-gold-search.md)
- [JD Gold Advanced Analysis](references/jdjr-gold-analysis-search.md)
- [JD Gold News Search](references/jdjr-news-search.md)
- [JD Gold Output Templates](references/output-templates.md)
- [Gold Holdings Diagnosis](references/黄金持仓诊断.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and concise user-facing text, with structured tables for holdings, prices, news, and simulated trading results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require JD account authorization for account-specific data; public market and news queries do not require login.]

## Skill Version(s):

1.0.0 (source: server evidence release.version and artifact/version.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
