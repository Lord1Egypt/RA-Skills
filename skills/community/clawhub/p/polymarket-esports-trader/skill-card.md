## Description:

Trades esports tournament, game release, and streaming milestone prediction markets on Polymarket using configurable paper or live execution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[diagnostikon](https://clawhub.ai/user/diagnostikon)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use this skill to discover esports and gaming prediction markets on Polymarket, size paper trades using configurable safeguards, and optionally place live orders after review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live mode can place real Polymarket orders with USDC.

Mitigation: Keep the skill in paper mode unless the strategy has been reviewed, and use account-side spending or order limits before live use.

Risk: The server security summary flags a risk-control gap in the live-trading path.

Mitigation: Enforce or remove the minimum-volume setting before live use, and confirm the configured position, spread, and open-position limits.

Risk: The server security summary flags an unpinned high-privilege dependency.

Mitigation: Pin and review simmer-sdk before installation or live execution.

Risk: SIMMER_API_KEY grants trading authority.

Mitigation: Use a tightly limited key and keep it scoped to the minimum permissions needed for the intended trading mode.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/diagnostikon/skills/polymarket-esports-trader)
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/)
- [simmer-sdk on GitHub](https://github.com/SpartanLabsXyz/simmer-sdk)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance and command-line text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can run in paper mode by default; live trading requires explicit use of the live flag and valid credentials.]

## Skill Version(s):

0.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
