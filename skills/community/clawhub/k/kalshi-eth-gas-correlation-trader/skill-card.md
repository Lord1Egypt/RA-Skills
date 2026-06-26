## Description: <br>
Trades ETH price markets on Kalshi using on-chain gas prices as a bullish/bearish signal. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[diagnostikon](https://clawhub.ai/user/diagnostikon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and trading agents use this skill to discover ETH-related Kalshi markets, estimate a gas-regime signal, and generate or execute bounded trade actions. It defaults to dry-run behavior and requires explicit live execution with configured trading credentials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use real credentials and place real trades when live execution is enabled. <br>
Mitigation: Keep the skill in dry-run until the strategy is reviewed, use a dedicated low-balance wallet and limited API key, and keep trade limits low. <br>
Risk: The gas signal may be estimated from market text rather than actual on-chain gas data. <br>
Mitigation: Do not assume live trades are based on actual on-chain gas data unless the code is changed to fetch and validate that feed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/diagnostikon/kalshi-eth-gas-correlation-trader) <br>
- [Simmer Skills](https://simmer.markets/skills) <br>
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/) <br>
- [simmer-sdk Repository](https://github.com/SpartanLabsXyz/simmer-sdk) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Console text and JSON automaton summaries, with Markdown setup and configuration guidance in the skill documentation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May execute live trades only when run with the explicit live flag and valid credentials; otherwise reports dry-run opportunities and configuration state.] <br>

## Skill Version(s): <br>
1.0.5 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
