## Description: <br>
Multi-strategy arbitrage and trading bot for Polymarket prediction markets. Scans ALL markets (crypto, politics, sports, economics, entertainment) for parity arbitrage, logical arbitrage, tail-end trading, market making, and latency opportunities. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[georges91560](https://clawhub.ai/user/georges91560) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External developers and traders use this skill to scan Polymarket prediction markets for arbitrage, market-making, and tail-end trading opportunities, with optional Telegram alerts and Polymarket API order placement. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Wallet private key exposure during setup or service deployment. <br>
Mitigation: Generate Polymarket API credentials locally, avoid placing WALLET_PRIVATE_KEY in runtime environments or systemd units, and run the service only with revocable API credentials. <br>
Risk: Real-money trading can lose funds or execute against flawed opportunity assumptions. <br>
Mitigation: Use a small dedicated wallet, set conservative capital limits, review opportunity logic before enabling authenticated order placement, and monitor logs and alerts during operation. <br>
Risk: Telegram alerts disclose trading signals and opportunity data to a third-party messaging service. <br>
Mitigation: Use Telegram only when acceptable for the deployment, restrict bot and chat access, or omit Telegram credentials to keep alerts local. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/georges91560/polymarket-oracle) <br>
- [Publisher profile](https://clawhub.ai/user/georges91560) <br>
- [Project repository and homepage](https://github.com/georges91560/polymarket-oracle) <br>
- [Polymarket CLOB API endpoint](https://clob.polymarket.com) <br>
- [Polymarket Gamma API endpoint](https://gamma-api.polymarket.com) <br>
- [Telegram Bot API endpoint](https://api.telegram.org/bot*) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Code, API Calls] <br>
**Output Format:** [Markdown guidance with inline shell commands, Python code, JSONL logs, console output, and Telegram messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Polymarket API credentials for authenticated trading; Telegram credentials are optional for alerts.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence; artifact frontmatter says 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
