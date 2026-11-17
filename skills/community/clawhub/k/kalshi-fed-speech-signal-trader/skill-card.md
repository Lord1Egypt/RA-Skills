## Description:

Trades Fed rate markets on Kalshi based on hawkish/dovish sentiment signals from market question text. Scores net sentiment from keyword dictionaries and adjusts rate cut probabilities. Requires SIMMER_API_KEY and simmer-sdk.

This skill is ready for commercial/non-commercial use.

## Publisher:

[diagnostikon](https://clawhub.ai/user/diagnostikon)

### License/Terms of Use:

MIT-0

## Use Case:

External ClawHub users and trading agents use this skill to discover Fed rate markets on Kalshi, score hawkish/dovish signals from market text, and propose or execute constrained trades through Simmer.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live exit logic can sell Fed-rate positions it did not create.

Mitigation: Use live mode only after reviewing open Fed-rate positions, and prefer a code or configuration change that restricts exits to positions tagged by this skill.

Risk: Dry-run mode can still change remote market state by importing markets.

Mitigation: Treat dry-run as capable of remote state changes, use low-limit credentials, and prevent remote imports during dry-run before relying on it as a no-impact test.

Risk: The skill can execute real-money trades when live mode is enabled with trading and wallet credentials.

Mitigation: Avoid live mode unless the user understands the DFlow/Solana trading path, use low-limit credentials, and pin simmer-sdk before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/diagnostikon/skills/kalshi-fed-speech-signal-trader)
- [Simmer skills homepage](https://simmer.markets/skills)
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/)
- [simmer-sdk repository](https://github.com/SpartanLabsXyz/simmer-sdk)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [Console text, JSON automaton status, and Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can run in dry-run mode by default or live mode when explicitly invoked with --live]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
