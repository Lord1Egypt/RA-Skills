## Description: <br>
基于盘前选股和实时行情，自动生成港股日内交易买入、卖出、止损价格及复盘结果，并可推送飞书消息。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aidalong](https://clawhub.ai/user/aidalong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Traders, analysts, and automation users can use this skill to prepare Hong Kong intraday stock plans, calculate target buy, sell, and stop-loss prices, review execution outcomes after market close, and generate concise trading review reports. Outputs should be reviewed before any real financial decision. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Trading outputs may be incorrect or based on simulated or stale market data. <br>
Mitigation: Confirm that every data path uses real, current market data and clearly label any simulated examples before using reports or signals. <br>
Risk: Feishu notifications may disclose trading details or send them to an unintended recipient. <br>
Mitigation: Review and replace the notification path, webhook configuration, and recipient settings before enabling push notifications. <br>
Risk: A Tushare token may be transmitted over cleartext HTTP. <br>
Mitigation: Rotate any exposed token and require a secure data access path before using Tushare-backed workflows. <br>
Risk: Shell execution behavior can increase command-injection exposure. <br>
Mitigation: Avoid shell=True and review command construction before running the scripts in an automated environment. <br>
Risk: Generated trading signals could be mistaken for financial advice. <br>
Mitigation: Treat outputs as review material only and require human financial judgment before real trades. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aidalong/hk-intraday-trading) <br>
- [Publisher profile](https://clawhub.ai/user/aidalong) <br>
- [Skill documentation](artifact/SKILL.md) <br>
- [Report template](artifact/template.md) <br>
- [Sample review report](artifact/examples/sample_report_2026-03-04.md) <br>
- [Eastmoney quote API used by the skill](https://push2.eastmoney.com/api/qt/stock/get) <br>
- [Tencent Finance quote API used by the skill](https://qt.gtimg.cn/q=hk00700) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, json, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown trading plans and review reports, JSON strategy and performance records, and shell or cron command snippets.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Feishu notification payloads and scheduled trading-day workflow guidance.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
