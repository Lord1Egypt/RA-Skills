## Description: <br>
Analyzes crypto wallets through the GMGN CLI/API, reporting holdings, realized and unrealized P&L, trading activity, performance stats, token balances, and developer-created tokens across Solana, BSC, Base, and Ethereum. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gmgnai](https://clawhub.ai/user/gmgnai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and analysts use this skill to inspect wallet holdings, P&L, win rate, activity history, token balances, and developer token launches before deciding whether to follow or copy-trade a wallet. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: First-time setup creates and stores sensitive GMGN credentials locally. <br>
Mitigation: Use a GMGN key with the least privileges available, store it only in ~/.config/gmgn/.env with restrictive file permissions, and remove any leftover /tmp/gmgn_private.pem file after setup. <br>
Risk: Wallet portfolio reports may expose sensitive financial activity. <br>
Mitigation: Treat generated wallet reports as sensitive financial data and avoid sharing raw outputs publicly. <br>
Risk: Repeated requests during GMGN rate-limit cooldowns can extend bans. <br>
Mitigation: Stop on rate-limit errors, read the reset time, and retry only after the reported cooldown expires. <br>


## Reference(s): <br>
- [GMGN Skill Portfolio on ClawHub](https://clawhub.ai/gmgnai/gmgn-portfolio) <br>
- [GMGN API key setup](https://gmgn.ai/ai) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown summaries and tables with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include wallet addresses, token addresses, transaction hashes, financial metrics, retry timing, and credential setup guidance.] <br>

## Skill Version(s): <br>
1.4.7 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
