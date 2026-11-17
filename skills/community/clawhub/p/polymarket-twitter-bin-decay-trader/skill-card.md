## Description:

Trades post-count bin markets by tracking elapsed time to identify mathematically dead bins that still hold residual probability.

This skill is ready for commercial/non-commercial use.

## Publisher:

[diagnostikon](https://clawhub.ai/user/diagnostikon)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and trading agents use this skill to evaluate and paper-trade Polymarket post-count bin markets based on elapsed-time viability signals. Live trading is available only through the explicit --live flag and requires separate operator review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live trading can place real Polymarket orders and the security evidence says some advertised safety limits are not actually enforced.

Mitigation: Keep the skill in paper mode unless the operator has audited the SDK and accepted the risk-control gaps.

Risk: A live-capable SIMMER_API_KEY could authorize trading if exposed to automated runtime use.

Mitigation: Use a narrowly scoped key, keep live credentials separate, and avoid providing a live-capable key unless --live operation is intended.

Risk: Final order size, liquidity, resolution timing, or existing open positions may differ from the strategy assumptions.

Mitigation: Verify order size, market liquidity, resolution timing, and open positions before enabling live execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/diagnostikon/skills/polymarket-twitter-bin-decay-trader)
- [Simmer Markets skills homepage](https://simmer.markets/skills)
- [simmer-sdk GitHub repository](https://github.com/SpartanLabsXyz/simmer-sdk)
- [simmer-sdk PyPI package](https://pypi.org/project/simmer-sdk/)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and runtime status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SIMMER_API_KEY and simmer-sdk; defaults to paper trading unless --live is passed.]

## Skill Version(s):

0.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
