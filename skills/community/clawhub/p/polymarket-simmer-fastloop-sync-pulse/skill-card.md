## Description: <br>
Trades Polymarket BTC, ETH, and SOL 5-minute fast markets using a Triple-Trigger strategy that combines Binance momentum, NOFX flow data, L2 wall detection, and pre-cached market IDs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AndrewBrownrd](https://clawhub.ai/user/AndrewBrownrd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External traders and agent operators use this skill to run or simulate automated Polymarket 5-minute market execution for BTC, ETH, and SOL. It supports paper-style runs without a wallet key and live trading only when a wallet private key is configured. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live mode can place real Polymarket trades when a wallet private key is configured. <br>
Mitigation: Start without WALLET_PRIVATE_KEY, confirm live mode intentionally, and use a dedicated low-balance wallet before allowing real USDC trading. <br>
Risk: Spend and position controls require manual review before relying on automation. <br>
Mitigation: Verify the actual code and configuration variable names for max position and daily budget, then test with conservative limits before scheduled operation. <br>
Risk: The managed five-minute schedule and local persistence files can affect repeated executions. <br>
Mitigation: Account for the managed schedule and review fast_markets_cache.json, daily_spend.json, and fastloop_ledger.json during deployment and troubleshooting. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/AndrewBrownrd/polymarket-simmer-fastloop-sync-pulse) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and configuration details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces trading run logs and local JSON state files when executed.] <br>

## Skill Version(s): <br>
1.0.7 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
