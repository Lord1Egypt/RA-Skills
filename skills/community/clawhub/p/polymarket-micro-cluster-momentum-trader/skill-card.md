## Description:

Trades cluster momentum continuation in 5-minute crypto Up/Down bundles on Polymarket when 2+ coins (BTC, ETH, SOL, XRP) show the same directional bias in one time slot, then trades continuation on the next slot at micro sizes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[diagnostikon](https://clawhub.ai/user/diagnostikon)

### License/Terms of Use:

MIT-0

## Use Case:

External agents and advanced trading operators use this skill to monitor Polymarket 5-minute crypto Up/Down bundles, detect same-direction cross-coin momentum clusters, and place paper or explicitly enabled live micro trades through Simmer.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live trading can place real USDC orders on Polymarket when enabled.

Mitigation: Run in paper mode first and require an explicit --live invocation only after reviewing configuration and account limits.

Risk: A persistent process that switches between paper and live execution can mislead operators about the active venue.

Mitigation: Avoid invoking live and paper runs in the same persistent process; start a fresh process for each mode.

Risk: Misconfigured trade sizing can cause minimum orders to exceed the intended maximum position.

Mitigation: Keep SIMMER_MIN_TRADE less than or equal to SIMMER_MAX_POSITION and review all tunables before enabling live trading.

Risk: SIMMER_API_KEY provides trading authority.

Mitigation: Scope and rotate the key, and store it only in the runtime secret mechanism intended for this skill.

Risk: The runtime dependency on simmer-sdk affects market discovery, configuration application, and trade execution.

Mitigation: Use a pinned, reviewed simmer-sdk version before enabling live trading.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/diagnostikon/skills/polymarket-micro-cluster-momentum-trader)
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/)
- [simmer-sdk GitHub repository](https://github.com/SpartanLabsXyz/simmer-sdk)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration]

**Output Format:** [Console text from a Python trading command, with environment-based configuration.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Paper trading is the default; live Polymarket trading requires the explicit --live flag and a SIMMER_API_KEY.]

## Skill Version(s):

0.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
