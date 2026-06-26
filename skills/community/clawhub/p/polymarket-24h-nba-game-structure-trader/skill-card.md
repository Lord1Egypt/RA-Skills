## Description: <br>
Trades structural inconsistencies across correlated NBA game markets on Polymarket by grouping moneyline, spread, O/U, and 1H markets for the same game and detecting cross-market mispricings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[diagnostikon](https://clawhub.ai/user/diagnostikon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and trading automation operators use this skill to discover correlated NBA Polymarket markets, check structural consistency, and test or run threshold-gated paper or live trades. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live execution can place real Polymarket trades and risk USDC. <br>
Mitigation: Test in paper mode first, review configured trade limits, and use --live only when prepared to accept real trading risk. <br>
Risk: SIMMER_API_KEY is a sensitive trading credential. <br>
Mitigation: Keep the key scoped, protected, and out of logs or shared configuration. <br>
Risk: The skill depends on an unpinned simmer-sdk package. <br>
Mitigation: Review the dependency version before deployment and pin or lock it in controlled environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/diagnostikon/polymarket-24h-nba-game-structure-trader) <br>
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/) <br>
- [simmer-sdk GitHub repository](https://github.com/SpartanLabsXyz/simmer-sdk) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Console output and Simmer or Polymarket trading actions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Defaults to paper trading; live execution requires --live and SIMMER_API_KEY.] <br>

## Skill Version(s): <br>
0.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
