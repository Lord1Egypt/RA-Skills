## Description: <br>
Trades CPI bin markets on Kalshi using the Cleveland Fed CPI Nowcast to compute fair bin probabilities via a normal distribution model. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[diagnostikon](https://clawhub.ai/user/diagnostikon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External traders and developers use this skill to evaluate CPI prediction-market bins and run a configurable Kalshi trading strategy through Simmer. It defaults to dry-run mode and only executes live trades when explicitly started with the live flag. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live mode can execute real-money Kalshi trades using USDC and a Solana private key. <br>
Mitigation: Keep the skill in dry-run mode until the trading venue, account, credentials, and order path are reviewed. <br>
Risk: Trading credentials and wallet keys are high-value secrets. <br>
Mitigation: Use a dedicated low-balance wallet and API key, and rotate or revoke credentials if exposure is suspected. <br>
Risk: Position sizing, slippage, liquidity, and trade frequency settings can materially affect losses. <br>
Mitigation: Set conservative max position, max trades, slippage, and liquidity limits before enabling live execution. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/diagnostikon/kalshi-econ-nowcast-trader) <br>
- [Simmer Skills](https://simmer.markets/skills) <br>
- [simmer-sdk GitHub repository](https://github.com/SpartanLabsXyz/simmer-sdk) <br>
- [simmer-sdk PyPI package](https://pypi.org/project/simmer-sdk/) <br>
- [Cleveland Fed Inflation Nowcasting](https://www.clevelandfed.org/indicators-and-data/inflation-nowcasting) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration, API calls] <br>
**Output Format:** [Terminal text output with optional automaton JSON status reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May place live trades only when explicitly run with the live flag and required credentials.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; skill frontmatter metadata lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
