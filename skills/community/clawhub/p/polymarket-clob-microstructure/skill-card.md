## Description:

Analyzes Polymarket CLOB order book microstructure to score liquidity gaps, order book imbalance, whale activity, and fake breakout patterns, then generates trading posture signals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mibayy](https://clawhub.ai/user/mibayy)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and trading operators use this skill to scan active Polymarket markets for order book microstructure inefficiencies, review ENTRY_OK, REDUCE_SIZE, SKIP, and MEAN_REVERT signals, and optionally run scheduled dry-run or live trading through Simmer.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can run repeatedly on a schedule with a trading API key and can place live trades when enabled.

Mitigation: Use a restricted SIMMER_API_KEY with account-side limits, keep dry-run mode until behavior is reviewed, and enable live trading only after operational testing.

Risk: The authoritative security evidence reports a fail-open context check before live trades.

Mitigation: Change the context check to fail closed before enabling scheduled live trading.

Risk: Unpinned runtime dependencies may change behavior after installation.

Mitigation: Pin simmer-sdk and requests to reviewed versions before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mibayy/skills/polymarket-clob-microstructure)
- [Publisher profile](https://clawhub.ai/user/mibayy)
- [Polymarket CLOB book API](https://clob.polymarket.com/book)
- [Polymarket trades API](https://data-api.polymarket.com/trades)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown usage guidance with bash commands and runtime text logs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SIMMER_API_KEY; defaults to dry-run mode and can execute live trades when invoked with --live.]

## Skill Version(s):

2.0.4 (source: server release evidence, skill frontmatter, and clawhub.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
