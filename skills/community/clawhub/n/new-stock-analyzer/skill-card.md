## Description: <br>
免费、实时、全面的A股新股分析工具。支持双数据源（东方财富+中财网），提供今日新股查询、基本面分析、风险评估、申购建议，直接在OpenClaw会话中发送通知。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[future2017](https://clawhub.ai/user/future2017) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and OpenClaw agents use this skill to query A-share IPO calendars, compare public market data sources, generate basic risk and valuation summaries, and send daily stock-analysis notifications. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup flow can install Python dependencies and add a persistent cron job for daily stock reports. <br>
Mitigation: Review the setup script before running it, install dependencies in a virtual environment, and enable cron only when persistent daily execution is desired. <br>
Risk: Scheduled jobs may continue running after testing or trial use. <br>
Mitigation: Check the user's crontab after testing and remove the entry when scheduled reports are no longer needed. <br>
Risk: Stock analysis, validation, and subscription suggestions may be mistaken for financial advice. <br>
Mitigation: Treat all analysis as informational and require users to make investment decisions based on their own judgment and risk tolerance. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/future2017/new-stock-analyzer) <br>
- [Publisher Profile](https://clawhub.ai/user/future2017) <br>
- [CFI New Stock Data](https://newstock.cfi.cn/) <br>
- [Eastmoney Data API](https://datacenter-web.eastmoney.com/api/data/v1/get) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and plain text reports with inline command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are informational market-data summaries and should not be treated as verified financial advice.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
