## Description: <br>
投资组合监控系统。管理股票、加密货币持仓，跟踪成本、盈亏，设置价格提醒，生成组合报告。支持港股、美股、加密货币。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sanduan003](https://clawhub.ai/user/sanduan003) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Investors and agents use this skill to review local stock and cryptocurrency holdings, fetch recent market prices, calculate gains and losses, and flag movements beyond a configured alert threshold. The output is for portfolio record keeping and monitoring, not investment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Portfolio configuration and generated state files can reveal holdings, cost basis, and symbols of interest. <br>
Mitigation: Keep memory/portfolio.json and the generated state file private, and avoid sharing them in logs, prompts, or support requests. <br>
Risk: Market data lookups disclose queried ticker symbols to yfinance/Yahoo Finance. <br>
Mitigation: Install and run the skill only if this external ticker-symbol disclosure is acceptable for the portfolio being monitored. <br>
Risk: The quick-start command uses --break-system-packages for Python package installation. <br>
Mitigation: Use a Python virtual environment for yfinance installation where possible. <br>
Risk: Portfolio calculations and alerts could be mistaken for investment advice. <br>
Mitigation: Treat outputs as record-keeping and monitoring aids only, and verify decisions through appropriate financial review. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sanduan003/portfolio-monitor) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, JSON files, guidance] <br>
**Output Format:** [Terminal text with local JSON configuration and state files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Fetches market data with yfinance and writes a local portfolio state summary.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
