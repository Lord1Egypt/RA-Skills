## Description: <br>
Trades structural inconsistencies across correlated NBA game markets on Polymarket by grouping moneyline, spread, O/U (full-game and 1H), and 1H moneyline markets for the same game and detecting cross-market mispricings including monotonicity violations, 1H-vs-full divergences, and spread-moneyline directional conflicts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[diagnostikon](https://clawhub.ai/user/diagnostikon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External traders and agent operators use this skill to discover NBA markets on Polymarket, group related game markets, detect structural pricing inconsistencies, and submit paper or explicitly enabled live trade orders through Simmer. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can place real Polymarket trades when run with the live flag. <br>
Mitigation: Start in paper mode, use --live only after accepting the risk of real USDC trades, and review all trade-size and threshold tunables before enabling live execution. <br>
Risk: SIMMER_API_KEY grants trading authority and is a high-value credential. <br>
Mitigation: Store the credential securely, limit access to trusted runtime environments, and rotate it if exposure is suspected. <br>
Risk: Market-structure signals may identify transient or noisy inconsistencies that do not produce profitable execution. <br>
Mitigation: Keep conservative limits for max position size, max open positions, minimum volume, maximum spread, and minimum inconsistency before allowing orders. <br>


## Reference(s): <br>
- [Simmer SDK on PyPI](https://pypi.org/project/simmer-sdk/) <br>
- [Simmer SDK GitHub Repository](https://github.com/SpartanLabsXyz/simmer-sdk) <br>
- [ClawHub Skill Page](https://clawhub.ai/diagnostikon/polymarket-48h-nba-game-structure-trader) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, shell commands, configuration, API calls, guidance] <br>
**Output Format:** [Text, Markdown, shell commands, and trade-order API requests] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Defaults to paper trading; live Polymarket execution requires the explicit --live flag and a SIMMER_API_KEY.] <br>

## Skill Version(s): <br>
0.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
