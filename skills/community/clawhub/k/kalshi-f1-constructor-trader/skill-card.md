## Description:

Trades F1 Drivers Championship markets on Kalshi using constructor (team) car performance ratings. Drivers in faster cars have structurally higher championship probabilities. Requires SIMMER_API_KEY and simmer-sdk.

This skill is ready for commercial/non-commercial use.

## Publisher:

[diagnostikon](https://clawhub.ai/user/diagnostikon)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and trading agents use this skill to analyze Kalshi F1 Drivers Championship markets with a constructor-performance model and to surface or execute position decisions under configured limits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live financial orders can be placed when the skill is run with live execution enabled.

Mitigation: Start in paper mode, review the live-trading risk before enabling --live, keep position and trade limits low, and monitor each run.

Risk: The skill depends on high-value trading and wallet credentials.

Mitigation: Use a limited API key and a dedicated low-balance wallet, and avoid providing SOLANA_PRIVATE_KEY unless live trading is intended.

Risk: The server security summary notes that live orders can proceed when safety context checks fail.

Mitigation: Review safety context results before execution and isolate or pin simmer-sdk before running with --live.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/diagnostikon/skills/kalshi-f1-constructor-trader)
- [Simmer Markets skills](https://simmer.markets/skills)
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/)
- [simmer-sdk repository](https://github.com/SpartanLabsXyz/simmer-sdk)

## Skill Output:

**Output Type(s):** [text, JSON, API calls, guidance]

**Output Format:** [Console text with optional automaton JSON status output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May place paper or live market orders through configured Simmer/Kalshi credentials when run with the selected execution mode.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
