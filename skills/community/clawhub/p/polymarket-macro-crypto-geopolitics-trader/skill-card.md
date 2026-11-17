## Description:

Trades geo-crypto divergence by comparing Polymarket geopolitical escalation probabilities with lagging crypto threshold markets and running paper-by-default trading logic before expected convergence.

This skill is ready for commercial/non-commercial use.

## Publisher:

[diagnostikon](https://clawhub.ai/user/diagnostikon)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and trading-agent operators use this skill to monitor Polymarket geopolitical and crypto threshold markets, detect divergence, and run paper-by-default trading logic that can be explicitly enabled for live Polymarket execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live use can place real Polymarket trades, and the server security summary says some documented financial safeguards are not strongly enforced for live trading.

Mitigation: Keep the skill in paper mode until liquidity, position-count, and sizing controls are reviewed and fixed; fund live accounts conservatively.

Risk: SIMMER_API_KEY grants trading authority.

Mitigation: Use a limited, revocable API key and rotate or revoke it if live execution is no longer needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/diagnostikon/skills/polymarket-macro-crypto-geopolitics-trader)
- [Simmer SDK on PyPI](https://pypi.org/project/simmer-sdk/)
- [Simmer SDK source repository](https://github.com/SpartanLabsXyz/simmer-sdk)

## Skill Output:

**Output Type(s):** [Text, Code, Shell commands, Configuration, API Calls]

**Output Format:** [Markdown guidance, Python code behavior, command-line output, and trade API requests]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Defaults to paper trading; live trading requires an explicit --live flag and SIMMER_API_KEY.]

## Skill Version(s):

0.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
