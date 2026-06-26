## Description: <br>
Trade Polymarket weather markets using NOAA (US) and Open-Meteo (international) forecasts via Simmer API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[simmer](https://clawhub.ai/user/simmer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent developers use this skill to inspect and automate Polymarket weather-market trading strategies, configure forecast and risk thresholds, run dry-run or paper trading, and intentionally opt into live execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live mode can place real orders and lose funds. <br>
Mitigation: Start in dry-run or TRADING_VENUE=sim, review markets and thresholds, keep position caps small, and pass --live only after wallet and API setup are intentional. <br>
Risk: Wallet and API credentials can enable trading if exposed. <br>
Mitigation: Avoid sharing broad wallet credentials, store SIMMER_API_KEY and WALLET_PRIVATE_KEY only in the runtime environment, and use the minimum access needed for the intended venue. <br>
Risk: Weather markets can gap at resolution with no stop-loss exit path. <br>
Mitigation: Size positions assuming the full position can go to zero; do not rely on percentage stop-loss monitors for gap-resolving temperature buckets. <br>
Risk: Forecast-source disagreement or missing station metadata can produce weak trade signals. <br>
Mitigation: Keep source-agreement checks enabled, review imported markets and thresholds, and skip or use small canary sizing when sources disagree. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/simmer/polymarket-weather-trader) <br>
- [Publisher profile](https://clawhub.ai/user/simmer) <br>
- [Wallet setup documentation](https://docs.simmer.markets/wallets) <br>
- [Polymarket V2 migration guide](https://docs.simmer.markets/v2-migration) <br>
- [Artifact disclaimer](artifact/DISCLAIMER.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration values] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include trading status, dry-run opportunities, position checks, and live-execution guidance depending on user intent and runtime flags.] <br>

## Skill Version(s): <br>
1.23.2 (source: release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
