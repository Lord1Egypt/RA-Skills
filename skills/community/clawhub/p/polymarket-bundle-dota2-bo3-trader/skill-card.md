## Description:

Trades structural inconsistencies between Dota 2 BO3 winner, individual game winners, and game handicap markets on Polymarket.

This skill is ready for commercial/non-commercial use.

## Publisher:

[diagnostikon](https://clawhub.ai/user/diagnostikon)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and trading agents use this skill to detect structural pricing inconsistencies across related Dota 2 BO3 Polymarket markets and, when explicitly enabled, place trades sized by the inconsistency signal.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live mode can place real-money Polymarket trades and cause USDC loss.

Mitigation: Keep the skill in paper mode unless live trading is intended, restrict the API key and account limits, and monitor positions outside the skill.

Risk: Important documented risk limits are not actually enforced according to the security evidence.

Mitigation: Do not rely on SIMMER_MIN_VOLUME or SIMMER_MAX_POSITIONS until those controls are fixed and reviewed.

Risk: The skill depends on simmer-sdk for market access and execution.

Mitigation: Pin and review simmer-sdk before production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/diagnostikon/skills/polymarket-bundle-dota2-bo3-trader)
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/)
- [simmer-sdk on GitHub](https://github.com/SpartanLabsXyz/simmer-sdk)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with Python and shell command references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SIMMER_API_KEY and simmer-sdk; defaults to paper trading unless live mode is explicitly enabled.]

## Skill Version(s):

0.0.3 (source: server release metadata; artifact frontmatter says 1.0.0 and clawhub.json says 0.0.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
