## Description:

Jarvis Stock Monitor is a stock, ETF, and gold monitoring and alerting skill for China-market workflows with cost, price-move, volume, moving-average, RSI, gap, trailing-stop, and tiered alerts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[15910701838](https://clawhub.ai/user/15910701838)

### License/Terms of Use:

MIT-0

## Use Case:

External users who monitor China-market stocks, ETFs, and gold use this skill to configure holdings, run price and technical alert checks, and receive tiered monitoring reports. The outputs are informational and do not replace financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Portfolio details are stored in local configuration and watched symbols or names are sent to external market-data services.

Mitigation: Use the skill only when that data sharing is acceptable, keep config.py private, and avoid committing portfolio details to version control.

Risk: The background monitor can continue making periodic market-data requests after it is started.

Mitigation: Start the daemon only when continuous monitoring is needed and stop it when monitoring is finished.

Risk: Notification credentials may be added to the optional Feishu or email configuration.

Mitigation: Keep webhook URLs and email credentials out of shared files and rotate them if they are exposed.

Risk: Generated alerts and trading suggestions may be incomplete, delayed, or misleading.

Mitigation: Treat outputs as informational signals and verify them against independent financial sources before making investment decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/15910701838/skills/jarvis-stock-monitor)
- [ClawHub publisher profile](https://clawhub.ai/user/15910701838)
- [Eastmoney quote API endpoint used by artifact](https://push2.eastmoney.com/api/qt/stock/get)
- [Sina Finance quote endpoint used by artifact](https://hq.sinajs.cn/list=)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python configuration snippets, shell commands, and text alert reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces informational monitoring alerts from locally configured watchlists and external market-data responses.]

## Skill Version(s):

1.0.0 (source: server release metadata, SKILL.md frontmatter, README.md, _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
