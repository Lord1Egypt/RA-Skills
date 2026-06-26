## Description: <br>
Polymarket 5-minute crypto UP/DOWN market automated trading bot that uses Binance technical analysis, Polymarket market data, and Polymarket CLOB order commands with gnosis-safe wallet mode. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hanguang254](https://clawhub.ai/user/hanguang254) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and trading operators use this skill to set up and run a bot that monitors 5-minute BTC/ETH Polymarket UP/DOWN markets, evaluates technical signals, places CLOB orders, and monitors positions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The artifact can place live Polymarket trades automatically from a funded wallet. <br>
Mitigation: Review before installing and require dry-run mode, explicit trade limits, manual approval, or a low-risk unfunded test setup before enabling live trading. <br>
Risk: The security evidence reports unsafe parsing of remote data. <br>
Mitigation: Remove unsafe parsing such as eval() and use structured JSON parsing with validation before running the bot. <br>
Risk: The security evidence reports fixed Telegram notification credentials in the artifact. <br>
Mitigation: Rotate any exposed Telegram credentials and replace them with user-controlled configuration or environment variables before use. <br>
Risk: The security evidence reports an external ai_trader dependency that is not packaged in the artifact. <br>
Mitigation: Package, pin, and review the dependency before installation or execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hanguang254/polymarket-5m-bot) <br>
- [Polymarket event page pattern](https://polymarket.com/event/{slug}) <br>
- [Polymarket Gamma event API pattern](https://gamma-api.polymarket.com/events?slug={slug}) <br>
- [Binance klines API](https://api.binance.com/api/v3/klines) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Code] <br>
**Output Format:** [Markdown with inline shell commands and Python code references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes trading setup guidance and scripts that interact with external market, exchange, notification, and order-execution services.] <br>

## Skill Version(s): <br>
3.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
