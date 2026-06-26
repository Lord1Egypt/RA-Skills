## Description: <br>
Tracks top Polymarket whale wallets, monitors leaderboard positions, and identifies high-conviction market signals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[themsquared](https://clawhub.ai/user/themsquared) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to inspect Polymarket leaderboard wallets, review open positions, and identify possible high-conviction market signals for research before making their own trading decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The script contacts Polymarket API endpoints and may send any wallet addresses a user queries. <br>
Mitigation: Install and run it only if that API contact is acceptable for the user's environment and wallet-address privacy expectations. <br>
Risk: The output is market research and may be incomplete, stale, or unsuitable as trading advice. <br>
Mitigation: Review the underlying markets and positions independently before acting, and do not treat the report as an automated trading system. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/themsquared/polymarket-whale-tracker-pro) <br>
- [Polymarket Data API](https://data-api.polymarket.com) <br>
- [Polymarket Gamma API](https://gamma-api.polymarket.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Terminal text report with wallet addresses, profile links, open-position tables, and recent-trade summaries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can run once, watch for periodic refreshes, or inspect a specific wallet address.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
