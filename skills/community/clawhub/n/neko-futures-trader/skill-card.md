## Description: <br>
Automates Binance Futures signal scanning, position monitoring, risk controls, and Telegram notifications for futures trading. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lukmanc405](https://clawhub.ai/user/lukmanc405) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to run an automated Binance Futures trading bot that scans markets, opens or manages positions, applies stop loss and take profit rules, and reports status through Telegram. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run as an autonomous Binance Futures trading bot and place live orders in the background. <br>
Mitigation: Use a Binance testnet or isolated low-balance account first, review the trading configuration, and remove or disable background startup behavior unless live autonomous trading is intended. <br>
Risk: Binance and Telegram credentials can expose funds, account data, or notification channels if mishandled. <br>
Mitigation: Disable withdrawals on API keys, restrict keys by IP, keep credentials out of logs and prompts, and never print `.env`. <br>
Risk: The dashboard can expose sensitive account data or workspace files if served publicly. <br>
Mitigation: Bind the dashboard to localhost or protect it with authentication, TLS, and firewall rules before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lukmanc405/neko-futures-trader) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/lukmanc405) <br>
- [Binance Futures](https://www.binance.com/en/futures) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, API calls, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands, configuration values, and Python runtime output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Binance and Telegram credentials; execution may start background processes and place live futures trades.] <br>

## Skill Version(s): <br>
1.0.27 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
