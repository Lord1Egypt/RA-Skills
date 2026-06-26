## Description: <br>
Autonomous Binance spot trading bot with LLM-powered market analysis. Supports momentum trading, mean reversion, and DCA strategies on any Binance spot pair. Use when user wants to trade on Binance, set up automated crypto trading, build a spot trading bot, or automate DCA buying. Features technical analysis, LLM sentiment evaluation, position sizing, and portfolio tracking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kirkraman](https://clawhub.ai/user/kirkraman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and crypto automation users use this skill to configure and run a Binance spot trading agent with technical indicators, LLM sentiment filtering, position sizing, and portfolio monitoring. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can place real Binance market orders automatically without a built-in dry-run mode, confirmation gate, or hard trading limits. <br>
Mitigation: Use a small isolated sub-account, require a dry-run or explicit approval before live trading, and add max trade size and daily loss limits before production use. <br>
Risk: The skill requires sensitive Binance credentials and a SkillBoss API key. <br>
Mitigation: Use Binance API keys with withdrawals disabled, apply IP restrictions, protect the host and environment files, and rotate keys if exposure is suspected. <br>
Risk: Market symbol, price, volume, and indicator context may be sent to the SkillBoss/heybossai LLM endpoint when LLM filtering is enabled. <br>
Mitigation: Review data-sharing acceptability before enabling LLM filtering, or disable LLM use when external market-context sharing is not acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kirkraman/godfery-binance-spot-trader) <br>
- [Publisher profile](https://clawhub.ai/user/kirkraman) <br>
- [OpenClaw homepage metadata](https://github.com/srikanthbellary) <br>
- [Binance REST API Reference](references/binance-api.md) <br>
- [Technical Indicators](references/indicators.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands, configuration examples, and Python scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Binance API credentials and a SkillBoss API key; produces runtime logs and trade history files when executed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
