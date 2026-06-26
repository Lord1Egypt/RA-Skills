## Description: <br>
Polymarket 5-minute crypto UP/DOWN market automated trading bot with AI-powered prediction using Binance technical analysis, automated betting through Polymarket CLOB API, and Gnosis Safe wallet mode. <br>

This skill is for research and development only. <br>

## Publisher: <br>
[hanguang254](https://clawhub.ai/user/hanguang254) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators can use this skill to configure, run, and monitor automated Polymarket crypto prediction-market trading workflows. The source documentation frames it as learning and research software and warns users to test thoroughly and avoid large funds. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can exercise real financial authority through automated prediction-market trading. <br>
Mitigation: Do not connect a funded wallet until the trading strategy, position limits, and background watchdog processes have been reviewed and tested in an isolated environment. <br>
Risk: The security evidence reports exposed secrets and under-disclosed external messaging. <br>
Mitigation: Remove hardcoded Telegram credentials, rotate exposed secrets, and delete wallet_backup.txt before any installation or deployment. <br>
Risk: The security evidence reports unsafe code paths and browser automation that need review. <br>
Mitigation: Replace eval with safe parsing and disable or isolate Chrome DevTools and browser automation before using the skill. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/hanguang254/polymarket-arb-bot) <br>
- [Polymarket Gamma API events endpoint](https://gamma-api.polymarket.com/events) <br>
- [Binance Kline API endpoint](https://api.binance.com/api/v3/klines) <br>
- [Binance API](https://api.binance.com) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with command examples and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May describe automated trading setup, monitoring commands, wallet configuration, and operational cautions.] <br>

## Skill Version(s): <br>
3.3.5 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
