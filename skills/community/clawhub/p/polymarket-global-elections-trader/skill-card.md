## Description:

Trades Polymarket prediction markets on elections, referendums, and democratic events worldwide using electoral-system heuristics and regional polling-lag signals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[diagnostikon](https://clawhub.ai/user/diagnostikon)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and trading agents use this skill to discover global election-related prediction markets, evaluate them with configurable election-bias rules, and place paper or explicitly enabled live trades through Simmer and Polymarket.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live trading can place real USDC orders when explicitly enabled.

Mitigation: Run in paper mode first and enable --live only after reviewing the trading logic and configured limits.

Risk: The server security summary reports weaker live-trading risk controls than documented.

Mitigation: Do not rely on the documented minimum-volume or maximum-open-position safeguards until they are fixed; enforce independent limits before live use.

Risk: The server security summary reports an unpinned simmer-sdk dependency.

Mitigation: Pin or review the simmer-sdk version before installing or running the skill.

Risk: SIMMER_API_KEY provides trading authority.

Mitigation: Use tightly scoped Simmer and Polymarket credentials and rotate them if exposed.

## Reference(s):

- [Polymarket Global Elections Trader on ClawHub](https://clawhub.ai/diagnostikon/skills/polymarket-global-elections-trader)
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/)
- [simmer-sdk on GitHub](https://github.com/SpartanLabsXyz/simmer-sdk)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, Python code, shell invocation, configuration values, and runtime status logs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SIMMER_API_KEY. Defaults to paper trading; live Polymarket trading requires an explicit --live flag.]

## Skill Version(s):

0.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
