## Description:

Trade prediction markets using LLM probability estimation enriched with real-time data from news, economic data, sports odds, political polling, and other sources.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mibayy](https://clawhub.ai/user/mibayy)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this automaton to estimate prediction-market probabilities from multiple public data sources and optionally execute Polymarket trades when estimates diverge from market prices.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The automaton can repeatedly make financial trades from LLM probability estimates influenced by external internet data.

Mitigation: Keep it in dry-run or paper trading until reviewed, and add fail-closed or manual-approval controls before enabling live trades.

Risk: Live operation can create financial exposure if trade size, market count, or divergence thresholds are misconfigured.

Mitigation: Set strict trade-size, exposure, market-scan, and threshold limits before scheduled execution.

Risk: The skill depends on trading, LLM, and optional data-provider API keys.

Mitigation: Use narrowly scoped, revocable credentials and review the configured LLM endpoint before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mibayy/skills/polymarket-multi-source-estimator)
- [Publisher profile](https://clawhub.ai/user/mibayy)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Command-line logs and trading actions configured through environment variables and command flags]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs on a managed cron schedule every 5 minutes; dry-run is the default unless live trading is explicitly enabled.]

## Skill Version(s):

1.1.4 (source: server release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
