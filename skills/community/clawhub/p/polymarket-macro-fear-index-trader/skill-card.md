## Description:

Builds a custom fear index from Polymarket markets by aggregating geopolitical, crypto, weather, and disease signals, then trades panic-discounted or complacency-overpriced markets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[diagnostikon](https://clawhub.ai/user/diagnostikon)

### License/Terms of Use:

MIT-0

## Use Case:

External users and trading agents use this skill to scan Polymarket markets, compute a macro fear index, and run paper or explicitly enabled live trading based on oversold and overpriced signals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live-trading safeguards do not fully enforce the advertised risk limits.

Mitigation: Use paper mode first, provide only a narrowly scoped and revocable SIMMER_API_KEY, and do not rely on documented max-position or minimum-volume safeguards unless the code is fixed or the venue enforces equivalent limits.

Risk: The skill can execute real Polymarket trades when live mode is explicitly enabled.

Mitigation: Review the skill and dependency before live use, keep live credentials separate from paper testing, and enable live mode only after confirming position limits and venue controls.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/diagnostikon/skills/polymarket-macro-fear-index-trader)
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/)
- [simmer-sdk on GitHub](https://github.com/SpartanLabsXyz/simmer-sdk)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown and command-line output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can place simulated or live trading orders depending on execution mode and credentials.]

## Skill Version(s):

0.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
