## Description:

Runs a configurable multi-timeframe momentum trading automation for SOL 5-minute fast markets using Binance SOL/USDT returns and Simmer market access.

This skill is ready for commercial/non-commercial use.

## Publisher:

[djdyll](https://clawhub.ai/user/djdyll)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and traders use this skill to run, tune, and monitor a SOL 5-minute momentum strategy that can operate in dry-run or live trading modes through Simmer.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can place real trades when live mode or scheduled automation is enabled.

Mitigation: Keep dry-run mode enabled until the strategy is tested, and enable cron or live trading only with explicit position sizing and risk limits.

Risk: A SIMMER_API_KEY is required for portfolio access and trading.

Mitigation: Use a minimally scoped key and avoid sharing logs or configuration that could expose credentials.

Risk: SIMMER_API_URL can redirect requests to a different endpoint.

Mitigation: Do not set SIMMER_API_URL unless the destination is fully trusted.

Risk: Dependency behavior depends on the installed simmer-sdk package.

Mitigation: Pin and review simmer-sdk before installation or deployment.

Risk: The release evidence flags a possible mismatch between SOL 5-minute trading through Simmer and references to BTC/Polymarket markets.

Mitigation: Confirm the intended market scope before enabling trading.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/djdyll/skills/polymarket-sol-5m-mtf-momentum-dyll)
- [Simmer API endpoint used by the skill](https://api.simmer.markets)
- [Binance kline API endpoint used by the skill](https://api.binance.com/api/v3/klines)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with Python scripts, JSON configuration, shell commands, status text, and optional automaton JSON reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SIMMER_API_KEY and simmer-sdk; can be configured with SIMMER_MTF_* environment variables.]

## Skill Version(s):

1.1.0 (source: server release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
