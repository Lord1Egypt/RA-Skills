## Description: <br>
Detects macro sentiment divergence across Polymarket prediction markets and trades against the stale side when positive- and negative-sentiment categories are priced high at the same time. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[diagnostikon](https://clawhub.ai/user/diagnostikon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and trading-agent operators use this skill to run a paper-by-default Polymarket strategy that identifies macro sentiment divergence, applies tunable risk limits, and can place live trades only when explicitly run with the live flag. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: SIMMER_API_KEY gives the skill trading authority. <br>
Mitigation: Install only if you are comfortable granting that authority, keep the credential secret, and start in paper mode. <br>
Risk: Live mode can place real Polymarket trades using USDC. <br>
Mitigation: Leave the default paper mode enabled until the strategy, thresholds, and position limits have been reviewed. <br>
Risk: The documented minimum-volume filter does not appear to be enforced in the included script. <br>
Mitigation: Verify market liquidity manually or add an enforced volume check before using live mode. <br>
Risk: The trading behavior depends on the external simmer-sdk package. <br>
Mitigation: Verify the simmer-sdk package and version before installation or execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/diagnostikon/polymarket-macro-sentiment-divergence-trader) <br>
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/) <br>
- [simmer-sdk on GitHub](https://github.com/SpartanLabsXyz/simmer-sdk) <br>


## Skill Output: <br>
**Output Type(s):** [Text, API Calls, Shell commands, Configuration] <br>
**Output Format:** [Console log text with Simmer or Polymarket trade requests] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Paper trading is the default; live trading requires SIMMER_API_KEY and an explicit live flag.] <br>

## Skill Version(s): <br>
0.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
