## Description: <br>
对持仓做一次性检查：盈亏、涨跌、缺口、均线与 RSI 等（无常驻进程，可配阈值与状态文件）。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jisuapi](https://clawhub.ai/user/jisuapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to run one-time checks on stock or ETF holdings from a local JSON configuration, then summarize triggered alerts for price movement, cost-based gain or loss, gaps, moving averages, volume changes, RSI, trailing profit, and cooldown suppression. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends monitored stock codes to JisuAPI and requires a JisuAPI key for quote and history lookups. <br>
Mitigation: Use the skill only when that data sharing is acceptable, keep JISU_API_KEY private, and avoid exposing the key in prompts, logs, or repositories. <br>
Risk: Local configuration and state files may include holding costs, stock codes, alert thresholds, and cooldown or trailing-profit state. <br>
Mitigation: Store local configuration and state files outside public repositories or add them to .gitignore, and restrict file permissions where appropriate. <br>
Risk: Market data and derived indicators may be delayed, incomplete, or unsuitable as financial advice. <br>
Mitigation: Treat results as informational alerts, verify important data independently, and avoid presenting outputs as buy, sell, or investment recommendations. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/jisuapi/jisu-stock-monitor) <br>
- [JisuAPI Stock API](https://www.jisuapi.com/api/stock/) <br>
- [JisuAPI Stock History API](https://www.jisuapi.com/api/stockhistory/) <br>
- [JisuAPI Website](https://www.jisuapi.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, JSON, guidance] <br>
**Output Format:** [JSON from the monitor script, with agent-facing Markdown or text summaries and shell commands for execution.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3, requests, JISU_API_KEY, monitored stock codes, and optional local state configuration.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
