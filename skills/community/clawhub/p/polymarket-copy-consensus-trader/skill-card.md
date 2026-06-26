## Description: <br>
Trades Polymarket markets only when at least three top whale wallets independently agree on direction, filtering single-wallet noise and scaling position size with consensus strength. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[diagnostikon](https://clawhub.ai/user/diagnostikon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and prediction-market operators use this skill to run a configurable Simmer/Polymarket trading bot that finds multi-wallet consensus signals, checks market safeguards, and executes paper or explicitly requested live trades. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live mode can execute real USDC trades when SIMMER_API_KEY is provided and --live is passed. <br>
Mitigation: Use paper mode first, pass --live only for intentional live trading, and keep max position and open-position tunables conservative. <br>
Risk: The SIMMER_API_KEY credential grants trading authority to the skill runtime. <br>
Mitigation: Keep the credential private and provide it only in environments where the operator accepts the trading authority granted to the skill. <br>
Risk: The skill depends on simmer-sdk for market access and execution. <br>
Mitigation: Review the simmer-sdk dependency before live use, especially before supplying live credentials. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/diagnostikon/polymarket-copy-consensus-trader) <br>
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/) <br>
- [simmer-sdk GitHub Repository](https://github.com/SpartanLabsXyz/simmer-sdk) <br>
- [predicting.top Leaderboard API](https://predicting.top/api/leaderboard) <br>
- [Polymarket Data API](https://data-api.polymarket.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration values] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May place simulated trades by default and live trades only when explicitly run with --live and valid trading credentials.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
