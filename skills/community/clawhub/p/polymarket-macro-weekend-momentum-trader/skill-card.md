## Description:

Trades ETH, SOL, and XRP Up/Down markets based on BTC weekend price-threshold momentum drift, defaulting to paper trading with optional live Polymarket execution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[diagnostikon](https://clawhub.ai/user/diagnostikon)

### License/Terms of Use:

MIT-0

## Use Case:

External traders and agent developers use this skill to run or adapt a weekend Polymarket macro strategy that compares BTC threshold-market drift with lagging ETH, SOL, and XRP Up/Down markets. It can be used in paper mode for evaluation or, with explicit live configuration, to place real trades.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live mode can place real Polymarket trades using SIMMER_API_KEY, and server security guidance warns that advertised volume and concurrent-position limits are not fully enforced.

Mitigation: Keep paper mode as the default; run with --live only after accepting the financial risk, using a restricted API key, small balances, and venue-side spending limits.

Risk: The trading strategy depends on weekend BTC-to-altcoin lag and can produce wrong or stale signals.

Mitigation: Review market conditions before enabling live trading and tune max position, minimum volume, spread, and drift thresholds conservatively.

Risk: The skill depends on simmer-sdk for market discovery, configuration, and order placement.

Mitigation: Install a pinned and verified simmer-sdk version before live use.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/diagnostikon/skills/polymarket-macro-weekend-momentum-trader)
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/)
- [simmer-sdk GitHub repository](https://github.com/SpartanLabsXyz/simmer-sdk)

## Skill Output:

**Output Type(s):** [Text, Code, Shell commands, Configuration, API calls, Guidance]

**Output Format:** [Markdown guidance, Python code, JSON configuration, and console log text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SIMMER_API_KEY and simmer-sdk; defaults to paper trading unless run with --live.]

## Skill Version(s):

0.0.3 (source: server release metadata; artifact frontmatter reports 1.0.0 and clawhub.json reports 0.0.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
