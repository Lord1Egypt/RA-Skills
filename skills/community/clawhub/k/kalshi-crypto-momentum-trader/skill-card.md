## Description:

Uses 7-day and 30-day price trend extrapolation to trade crypto year-end price target markets on Kalshi and requires SIMMER_API_KEY plus simmer-sdk.

This skill is ready for commercial/non-commercial use.

## Publisher:

[diagnostikon](https://clawhub.ai/user/diagnostikon)

### License/Terms of Use:

MIT-0

## Use Case:

Agents use this skill to evaluate Kalshi crypto year-end price target markets and, when explicitly enabled, place bounded live trades from momentum-derived edge signals. It is intended for operators who can manage trading credentials, position limits, and strategy review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires high-value trading credentials and can place live trades when --live is supplied.

Mitigation: Use a dedicated low-value wallet and tightly scoped trading API key; keep live mode disabled until credentials, limits, and strategy behavior have been reviewed.

Risk: The live strategy may rely on hardcoded market assumptions rather than fresh price data.

Mitigation: Do not enable --live until the strategy is connected to fresh price data and its momentum assumptions are validated.

Risk: Dry-run mode is non-trading but may still import markets into the remote platform.

Mitigation: Test in an isolated account or workspace and review remote-side effects before routine use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/diagnostikon/skills/kalshi-crypto-momentum-trader)
- [Publisher Profile](https://clawhub.ai/user/diagnostikon)
- [Simmer Skills](https://simmer.markets/skills)
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/)
- [simmer-sdk Repository](https://github.com/SpartanLabsXyz/simmer-sdk)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [Console text with optional JSON automaton status and configuration updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can perform dry-run analysis by default and live trading actions only when --live is supplied.]

## Skill Version(s):

1.0.5 (source: server release evidence; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
