## Description:

Trade Polymarket 5-minute crypto fast markets using 1-minute candle body analysis and volume surge detection from Binance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mibayy](https://clawhub.ai/user/mibayy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and trading automation users use this skill to run or adapt a Polymarket fast-market trading script that scans crypto candle and volume signals, selects the strongest asset signal, and dry-runs or places trades through Simmer.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live mode can place real-money Polymarket trades automatically.

Mitigation: Keep dry-run enabled until the strategy and configuration are reviewed, then use small position limits and a tightly limited Simmer API key for any live run.

Risk: A pre-trade safety check can fail open when context is unavailable.

Mitigation: Avoid unattended live cron operation until this behavior is fixed or independently guarded by an external stop condition.

Risk: The skill depends on external market data, trading APIs, and Python packages.

Mitigation: Pin and review dependencies before live use, monitor API failures, and verify signal behavior against current market conditions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mibayy/skills/polymarket-candle-momentum)
- [Binance public klines API](https://api.binance.com/api/v3/klines)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown and terminal text with inline shell commands and JSON configuration output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Dry-run is the default; live mode requires an explicit --live flag and SIMMER_API_KEY.]

## Skill Version(s):

2.0.0 (source: server release evidence and clawhub.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
