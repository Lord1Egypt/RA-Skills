## Description: <br>
World Cup Groups skill — a market-dynamics play on group-winner sets that buys group favorites at pre-tournament prices, trims after qualification becomes market-obvious, and trades incoherent group market sets back toward consistency. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bridgeaisocial](https://clawhub.ai/user/bridgeaisocial) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and trading operators use this skill to run a Simmer-based paper or live prediction-market workflow for 2026 World Cup group-winner markets. It discovers active and importable group markets, reports candidate sets, and, when explicitly configured for live trading, places bounded trades using the configured venue. <br>

### Deployment Geography for Use: <br>
Global, subject to local eligibility and compliance requirements for prediction-market trading. <br>

## Known Risks and Mitigations: <br>
Risk: Live automated trading can lose money through adverse prices, slippage, illiquidity, or incorrect configuration. <br>
Mitigation: Keep the skill in dry-run mode until the strategy and settings are reviewed; verify live mode, venue, spending limits, and position limits before enabling real-money execution. <br>
Risk: The skill requires API keys or wallet-linked credentials for trading workflows. <br>
Mitigation: Store credentials only in a secured environment and restrict access to the account or agent that runs the skill. <br>
Risk: Group-set trades are sequential and may face partial fills or market movement. <br>
Mitigation: Use small per-trade caps, the configured exposure cap, and slippage checks; review incomplete or unconfirmed market sets before live execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bridgeaisocial/polymarket-worldcup-group-repricer) <br>
- [Publisher profile](https://clawhub.ai/user/bridgeaisocial) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash examples and text reports from Python scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Default dry-run mode uses the Simmer paper engine; live mode can call trading APIs, emit reasoning strings, and update local exposure state.] <br>

## Skill Version(s): <br>
0.2.0 (source: ClawHub release metadata and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
