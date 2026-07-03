## Description: <br>
Trade Kalshi soccer markets using EA FC OVR rating disparity and a bivariate Poisson model. Finds edge on match winner, total goals (over/under), and goal spread markets. Use when the user wants to trade soccer markets on Kalshi, automate soccer bets using FIFA ratings, or find mispriced soccer outcomes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bridgeaisocial](https://clawhub.ai/user/bridgeaisocial) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and traders use this skill to evaluate Kalshi soccer markets, dry-run or execute wallet-based trades, and manage positions using EA FC ratings, lineup data, and a bivariate Poisson goal model. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can execute automated real-money prediction market trades using a Solana wallet. <br>
Mitigation: Start in dry-run mode, use a dedicated low-balance wallet, keep small position limits, and avoid disabling safeguards. <br>
Risk: The artifact includes a stealth SoFIFA scraper intended to bypass bot protection. <br>
Mitigation: Review or remove the scraper before use if the site-access or compliance risk is unacceptable. <br>
Risk: The skill requires sensitive credentials, including a Simmer API key and a Solana private key for live trading. <br>
Mitigation: Store credentials outside source control, restrict wallet funds, and rotate secrets if exposure is suspected. <br>
Risk: The model and rating data may produce incorrect probabilities and financial losses. <br>
Mitigation: Treat results as decision support, verify market settlement rules, backtest or dry-run first, and use small trade sizes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bridgeaisocial/kalshi-fifa-soccer-trader) <br>
- [SoFIFA team ratings](https://sofifa.com/teams?type=international&col=oa&sort=desc) <br>
- [TheSportsDB API](https://www.thesportsdb.com/api/v1/json/3) <br>
- [Wikipedia API](https://en.wikipedia.org/w/api.php) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands, configuration values, and code-oriented guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes dry-run and live-trading commands, environment variables, risk thresholds, and position-management guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
