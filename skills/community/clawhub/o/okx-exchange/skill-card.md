## Description: <br>
OKX Exchange is a quantitative trading agent for OKX that supports market data, account management, order execution, automated strategies, risk monitoring, and reports across spot, perpetual swaps, and futures. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lk2023060901](https://clawhub.ai/user/lk2023060901) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to query OKX market and account data, manage positions, execute trades, run grid, trend, and arbitrage strategies, monitor liquidation and stop-loss/take-profit risk, and generate performance reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access OKX account data and, when configured, place live trades or transfer funds. <br>
Mitigation: Start in paper trading, use OKX API keys with the minimum permissions needed, keep order confirmation enabled, and configure position, leverage, and daily trade limits before live use. <br>
Risk: Automated monitoring, cron jobs, auto_trade, or --no-confirm can execute trading actions without an interactive prompt. <br>
Mitigation: Do not enable auto_trade, cron jobs, or confirmation bypasses until limits are configured and behavior has been tested in paper trading; use the documented teardown command as a kill switch. <br>
Risk: A custom OKX_API_URL can route account and trading requests to a nonstandard endpoint. <br>
Mitigation: Avoid setting OKX_API_URL unless the endpoint is controlled and trusted. <br>
Risk: API credentials grant access to financial account data and trading authority. <br>
Mitigation: Store credentials outside the published skill, avoid logging or printing secrets, and keep live and demo credentials isolated. <br>


## Reference(s): <br>
- [OKX V5 API Documentation](https://www.okx.com/docs-v5/en/) <br>
- [OKX API Key Management](https://www.okx.com/account/my-api) <br>
- [Trading Rules](artifact/docs/trading-rules.md) <br>
- [Decision Engine Guide](artifact/docs/decision-engine-guide.md) <br>
- [Learning System Data Management](artifact/docs/learning-system-data-management.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown and plain text reports with shell command guidance and JSON-backed configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read and write local memory files and call OKX APIs when the agent runs the provided commands.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
