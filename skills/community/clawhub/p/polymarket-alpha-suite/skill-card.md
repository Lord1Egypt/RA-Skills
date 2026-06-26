## Description: <br>
Six Polymarket market-scanning and trading-signal tools for NegRisk arbitrage, latency arbitrage, BTC scalping, alpha scanning, universe scanning, and edge detection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aiagent234-bit](https://clawhub.ai/user/aiagent234-bit) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Prediction-market traders and agent operators use this skill to scan Polymarket markets, surface possible arbitrage or edge opportunities, and run paper-trading workflows before considering manual or live execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks for wallet or API credentials for live trading, and the security evidence warns not to use a primary wallet private key. <br>
Mitigation: Use paper-trading mode first, use a separate low-balance trading wallet or limited-scope API credentials, and keep any .env file out of version control. <br>
Risk: The security evidence rates the release as suspicious and notes that the code mostly scans markets and records paper-trading signals rather than independently verified live order placement. <br>
Mitigation: Treat results as market-scanning signals, manually verify order books and market conditions before trading, and avoid relying on claimed performance as a guarantee. <br>
Risk: Local output files may reveal trading interests or strategy history. <br>
Mitigation: Store generated data files locally with appropriate access controls and remove them when they are no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/aiagent234-bit/polymarket-alpha-suite) <br>
- [README](README.md) <br>
- [Setup guide](SETUP.md) <br>
- [Polymarket](https://polymarket.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and optional JSON files written by the tools] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Some tools can save local JSON history or market-analysis files under data/.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
