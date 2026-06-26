## Description: <br>
Trades F1 Drivers Championship markets on Kalshi using constructor (team) car performance ratings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[diagnostikon](https://clawhub.ai/user/diagnostikon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to evaluate Kalshi F1 Drivers Championship markets, identify constructor-rating edges, and optionally execute trades after explicit live-mode activation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live mode can place real-money Kalshi trades using wallet and API credentials. <br>
Mitigation: Run in dry-run mode first, use dedicated low-value credentials, and pass --live only after accepting the trading risk. <br>
Risk: Exit logic may sell broader F1 positions rather than only positions opened by this skill. <br>
Mitigation: Review or modify the exit logic to sell only positions tagged with this skill before using it with existing F1 holdings. <br>
Risk: The strategy relies on static constructor ratings and tunable thresholds. <br>
Mitigation: Review the model assumptions and tune position size, edge, slippage, liquidity, and trade-count limits before live use. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/diagnostikon/kalshi-f1-constructor-trader) <br>
- [Simmer Markets Skills](https://simmer.markets/skills) <br>
- [simmer-sdk Repository](https://github.com/SpartanLabsXyz/simmer-sdk) <br>
- [simmer-sdk PyPI Package](https://pypi.org/project/simmer-sdk/) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text logs, JSON automaton status, and command-line guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Dry-run by default; live trading requires the explicit --live flag and configured credentials.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
