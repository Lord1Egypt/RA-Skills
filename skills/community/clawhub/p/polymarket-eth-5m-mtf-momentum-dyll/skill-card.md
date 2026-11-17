## Description:

Configurable Simmer trading bot that aligns 1m/3m/5m Binance ETH/USDT returns to trade directional Polymarket five-minute fast markets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[djdyll](https://clawhub.ai/user/djdyll)

### License/Terms of Use:

MIT-0

## Use Case:

External traders and developers use this skill as a configurable Simmer trading bot for ETH 5-minute fast markets, using Binance ETH/USDT momentum across 1-minute, 3-minute, and 5-minute windows to decide whether to place directional trades. It supports paper runs, live runs, position checks, configuration updates, and scheduled execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can place live trades when run with --live or scheduled after configuration.

Mitigation: Run in paper mode first, tune confidence and timing thresholds, review active safeguards, and enable live trading only with an accepted loss limit.

Risk: The trading API key is sent to a configurable Simmer endpoint.

Mitigation: Use a dedicated low-scope Simmer key and set SIMMER_API_URL only to a trusted HTTPS Simmer endpoint.

Risk: Evidence flags an ETH versus BTC description mismatch that could confuse market selection or user expectations.

Mitigation: Confirm the target asset and market wording before deployment; treat the current implementation as ETH-focused unless the code and docs are corrected together.

Risk: The skill depends on the external simmer-sdk package for trading behavior.

Mitigation: Pin and review the simmer-sdk version before production use.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, shell commands, configuration, code, API calls]

**Output Format:** [Console text with optional JSON automaton report and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SIMMER_API_KEY, simmer-sdk, and review before live trading or scheduled execution.]

## Skill Version(s):

1.1.0 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
