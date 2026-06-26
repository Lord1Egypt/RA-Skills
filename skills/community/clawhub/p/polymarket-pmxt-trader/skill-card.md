## Description: <br>
Trade Polymarket using PMXT cross-exchange predictions and orderbook data for entry/exit signals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[senarokalie](https://clawhub.ai/user/senarokalie) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and trading-agent operators use this skill to run a configurable Polymarket trading workflow that pulls PMXT market signals, applies liquidity and price filters, and can simulate or execute trades through Simmer. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can place real-money Polymarket trades and redeem positions when live or recurring execution is enabled. <br>
Mitigation: Use dry-run first, keep live execution disabled until reviewed, and only enable live or recurring runs when the operator accepts automated trading and redemption. <br>
Risk: The skill requires sensitive API keys and may use wallet credentials for self-custody trading. <br>
Mitigation: Use isolated credentials or a limited wallet, restrict balances and permissions, and rotate credentials if exposed. <br>
Risk: Automated strategy settings can create repeated trades if thresholds, position caps, or schedules are too broad. <br>
Mitigation: Keep per-trade and per-run caps small, review threshold settings, and monitor runs before increasing limits. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/senarokalie/polymarket-pmxt-trader) <br>
- [PMXT](https://pmxt.dev) <br>
- [PMXT API endpoint](https://api.pmxt.dev/api) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Shell commands, Configuration, API calls, Text] <br>
**Output Format:** [Python script output, CLI commands, and environment-variable configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SIMMER_API_KEY and PMXT_API_KEY; dry run is default, while live trading requires the --live flag.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
