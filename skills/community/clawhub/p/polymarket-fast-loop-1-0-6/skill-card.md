## Description: <br>
Trade Polymarket BTC 5-minute and 15-minute fast markets using CEX price momentum signals via Simmer API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[johnjerry8749](https://clawhub.ai/user/johnjerry8749) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agent operators use this skill to configure and run a Polymarket fast-market trading loop that compares short-window crypto price momentum against market odds. It is dry-run by default, but can place real USDC trades when run with live trading enabled. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can execute automated real-money Polymarket trades when live mode is enabled. <br>
Mitigation: Run dry-run first, review the selected market and signal output, set max_position explicitly, and enable live mode only with approved trading limits. <br>
Risk: Cron or heartbeat loops can repeatedly trigger live trading without additional stop-loss or spend controls. <br>
Mitigation: Avoid unattended live loops unless external monitoring, hard spend limits, and stop/loss controls are in place. <br>
Risk: The skill requires a Simmer API key for account-backed trading actions. <br>
Mitigation: Use a dedicated key that can be revoked quickly and store it only in the runtime environment. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/johnjerry8749/polymarket-fast-loop-1-0-6) <br>
- [Simmer API](https://api.simmer.markets) <br>
- [Polymarket Gamma Markets API](https://gamma-api.polymarket.com/markets) <br>
- [Binance Klines API](https://api.binance.com/api/v3/klines) <br>
- [CoinGecko Simple Price API](https://api.coingecko.com/api/v3/simple/price) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with shell commands, JSON configuration, and terminal status output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SIMMER_API_KEY; produces dry-run or live-trading status output and may update config.json through CLI settings.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata; artifact frontmatter reports 1.0.6) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
