## Description: <br>
Trade Polymarket SOL, BTC, and ETH prediction markets using live Solana on-chain signals from public Solana RPC and Jupiter data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chokle](https://clawhub.ai/user/chokle) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and trading agents use this skill to collect Solana network activity, derive a composite bullish/neutral/bearish signal, and trade matching crypto prediction markets through Simmer. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run unattended live trades on a schedule when configured with a Simmer API key. <br>
Mitigation: Use a least-privilege Simmer key, confirm whether TRADING_VENUE targets simulation or real-money trading, reduce position and trade limits, and disable the cron or automaton unless unattended live trading is intended. <br>
Risk: The security review reports that live trading risk is not clearly disclosed or gated. <br>
Mitigation: Review the skill before deployment, run --signals and dry-run modes first, and require an explicit live-trading approval path before enabling --live execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chokle/polymarket-solana-onchain) <br>
- [Simmer docs](https://docs.simmer.markets) <br>
- [Solana RPC docs](https://docs.solana.com/api/http) <br>
- [Jupiter stats API](https://stats.jup.ag) <br>
- [Helius RPC](https://helius.dev) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash commands; strategy runs produce console logs and optional JSON automaton status.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SIMMER_API_KEY for trading; clawhub.json configures a managed live automaton on a 10-minute cron.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
