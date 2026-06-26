## Description: <br>
Trade Polymarket "Elon Musk # tweets" markets using XTracker post count data by identifying adjacent range buckets whose combined cost is below the configured threshold. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[simmer](https://clawhub.ai/user/simmer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External traders and agent operators use this skill to monitor Elon Musk tweet-count markets, review XTracker pace data, configure bucket-trading thresholds, and run dry-run or live Simmer/Polymarket trading workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can place real market trades when live mode is enabled. <br>
Mitigation: Start in dry-run mode, review trade proposals and configuration, keep position limits conservative, and enable live mode only after understanding the strategy and venue risks. <br>
Risk: Self-custody live trading may require highly sensitive wallet access. <br>
Mitigation: Prefer managed-wallet or safer signing flows; if a private key is required, use a dedicated low-balance wallet rather than a production wallet. <br>
Risk: Status and portfolio output can reveal sensitive financial account data. <br>
Mitigation: Treat status output, logs, screenshots, and shared terminal transcripts as sensitive. <br>
Risk: Automated trading can lose money because market conditions, signal lag, slippage, and configuration errors may invalidate the strategy. <br>
Mitigation: Run paper or dry-run mode first, review slippage and safeguard settings, and size positions conservatively. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/simmer/polymarket-elon-tweets) <br>
- [Simmer dashboard](https://simmer.markets/dashboard) <br>
- [Simmer API base](https://api.simmer.markets) <br>
- [Simmer Polymarket V2 migration guide](https://docs.simmer.markets/v2-migration) <br>
- [Skill disclaimer](DISCLAIMER.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with command examples, terminal output, and JSON-backed configuration.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce dry-run trading summaries, status reports, configuration updates, and live-trading instructions.] <br>

## Skill Version(s): <br>
1.3.5 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
