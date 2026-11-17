## Description:

Trades crypto "Up or Down" 5-minute interval markets on Polymarket by detecting Morning Star and Evening Star candlestick reversal patterns and sizing trades from the apparent lag in the next interval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[diagnostikon](https://clawhub.ai/user/diagnostikon)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent builders use this skill to scan Polymarket crypto interval markets for Morning Star and Evening Star reversal patterns, then produce paper trades by default or live orders when explicitly enabled.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live trading can place real USDC orders while some promised risk controls are not fully enforced.

Mitigation: Use paper trading unless live-risk controls have been reviewed, fixed, and backed by external trading limits.

Risk: The required SIMMER_API_KEY grants trading authority.

Mitigation: Use a narrowly scoped key, protect it as a high-value credential, and rotate it if exposure is suspected.

Risk: The skill depends on the external simmer-sdk package for market access and order placement.

Mitigation: Pin simmer-sdk to a reviewed version before enabling live trading.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/diagnostikon/skills/polymarket-candle-morning-star-trader)
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/)
- [simmer-sdk GitHub repository](https://github.com/SpartanLabsXyz/simmer-sdk)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with command-line examples and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces trading decisions through the Simmer SDK; default execution mode is paper trading unless live mode is explicitly selected.]

## Skill Version(s):

0.0.3 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
