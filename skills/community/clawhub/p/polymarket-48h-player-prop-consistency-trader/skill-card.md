## Description: <br>
Trades NBA player prop mispricings on Polymarket by detecting cross-stat consistency or divergence for the same player (Points, Rebounds, Assists O/U) and identifying outlier stats that disagree with the consensus direction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[diagnostikon](https://clawhub.ai/user/diagnostikon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and developers use this skill to discover NBA player prop markets, compare a player's points, rebounds, and assists lines for consistency, and place paper trades by default through the Simmer SDK. It can place live Polymarket trades only when explicitly run with the live flag. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can place live Polymarket trades with real USDC when run with the live flag. <br>
Mitigation: Start in paper mode, keep position limits low, and use --live only when prepared to accept real financial risk. <br>
Risk: The required SIMMER_API_KEY grants access to trading functionality. <br>
Mitigation: Store the API key securely, limit its permissions where possible, and review Simmer SDK behavior before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/diagnostikon/polymarket-48h-player-prop-consistency-trader) <br>
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/) <br>
- [simmer-sdk on GitHub](https://github.com/SpartanLabsXyz/simmer-sdk) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Console logs, command-line flags, and environment-based configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SIMMER_API_KEY; defaults to simulated trading unless run with --live.] <br>

## Skill Version(s): <br>
0.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
