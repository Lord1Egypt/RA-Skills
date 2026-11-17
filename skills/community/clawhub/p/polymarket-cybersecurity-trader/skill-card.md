## Description:

Trades Polymarket prediction markets on major cyberattacks, ransomware incidents, data breaches, zero-day exploits, and national cybersecurity legislation using keyword market discovery, conviction-based sizing, and cybersecurity timing signals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[diagnostikon](https://clawhub.ai/user/diagnostikon)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and trading agents use this skill to discover cybersecurity-related Polymarket markets, evaluate signal thresholds, and place paper or live trades through Simmer. The default posture is paper trading, with real-money trading only when live execution is explicitly enabled.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live-trading safety controls have material gaps that could cause unintended real-money trades.

Mitigation: Start in paper mode, use live mode only after review, require an additional live-trading confirmation, and keep position-size tunables capped.

Risk: The required SIMMER_API_KEY is a high-value trading credential.

Mitigation: Use a limited-risk key, avoid broad account permissions where possible, and rotate the key if it may have been exposed.

Risk: The external simmer-sdk dependency may change behavior if left unpinned.

Mitigation: Pin and review the dependency before enabling real-money trading.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/diagnostikon/skills/polymarket-cybersecurity-trader)
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/)
- [simmer-sdk on GitHub](https://github.com/SpartanLabsXyz/simmer-sdk)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python code behavior, command-line usage, and configuration parameters]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SIMMER_API_KEY and simmer-sdk; default execution is paper trading unless live mode is explicitly enabled.]

## Skill Version(s):

0.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
