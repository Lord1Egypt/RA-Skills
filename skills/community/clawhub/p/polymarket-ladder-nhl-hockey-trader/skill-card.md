## Description:

Trades monotonicity violations in NHL hockey O/U market ladders and spread-vs-total consistency on Polymarket, where each game can have multiple O/U lines that should decrease as totals rise.

This skill is ready for commercial/non-commercial use.

## Publisher:

[diagnostikon](https://clawhub.ai/user/diagnostikon)

### License/Terms of Use:

MIT-0

## Use Case:

External agents and developers use this skill to scan Polymarket NHL over/under and spread markets, identify ladder inconsistencies, and place simulated or live trades through Simmer when configured.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live mode can create real-money Polymarket exposure, and the security summary warns expected paper-trading safeguards may be violated.

Mitigation: Use a restricted SIMMER_API_KEY with minimal funds and permissions, and verify the venue and live flag in an isolated worker before any funded run.

Risk: Volume and max-position controls are described by security guidance as incomplete.

Mitigation: Review and fix risk-limit enforcement before live use, keep SIMMER_MAX_POSITION, SIMMER_MAX_POSITIONS, SIMMER_MIN_VOLUME, and trade thresholds conservative, and monitor orders manually.

Risk: Paper mode may not be reliable in a persistent worker after any live run.

Mitigation: Separate live and paper deployments or restart the worker and confirm the venue is sim before paper testing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/diagnostikon/skills/polymarket-ladder-nhl-hockey-trader)
- [Simmer SDK on PyPI](https://pypi.org/project/simmer-sdk/)
- [Simmer SDK GitHub repository](https://github.com/SpartanLabsXyz/simmer-sdk)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, code, guidance]

**Output Format:** [Markdown guidance, Python code, configuration values, shell commands, and console status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can execute simulated trades by default and live Polymarket trades when explicitly run with live mode.]

## Skill Version(s):

0.0.3 (source: server-resolved release metadata; artifact frontmatter reports 1.0.0 and clawhub.json reports 0.0.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
