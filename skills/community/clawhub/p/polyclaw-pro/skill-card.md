## Description: <br>
Trade on Polymarket via split and CLOB execution, browse markets, track positions with P&L, discover hedges with LLM analysis, and use automation tools for live portfolio tracking, auto-redeem, discipline scanning, and an API bridge on Polygon/Web3. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lmanchu](https://clawhub.ai/user/lmanchu) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to browse Polymarket markets, manage wallet-backed prediction-market positions, execute trades, monitor live portfolio P&L, and identify hedge opportunities. It is intended for agents operating with user-provided wallet and API credentials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent live wallet authority for trading, approvals, redemptions, swaps, and other financial actions. <br>
Mitigation: Use a fresh low-balance wallet, keep only funds you can afford to risk, and manually review each command before enabling automated execution. <br>
Risk: Cron automation and the API bridge can trigger financial actions without interactive review. <br>
Mitigation: Do not enable cron jobs or delegated API/SSH access until the code, risk rules, environment, and wallet addresses have been reviewed. <br>
Risk: Hard-coded wallet or funder addresses and missing delegated-trading modules may make behavior differ from the user's intended account or fail at runtime. <br>
Mitigation: Correct wallet and funder configuration for the deployment account and verify all required modules before running buy, sell, redeem, approve, or swap flows. <br>


## Reference(s): <br>
- [ClawHub PolyClaw Pro release](https://clawhub.ai/lmanchu/polyclaw-pro) <br>
- [Polymarket](https://polymarket.com) <br>
- [PolyClaw video explainer](https://www.youtube.com/watch?v=s_uP802NVTE) <br>
- [Chainstack console](https://console.chainstack.com) <br>
- [OpenRouter API keys](https://openrouter.ai/settings/keys) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and terminal text with optional structured JSON outputs from CLI/API bridge commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can initiate live wallet, approval, buy, sell, redeem, swap, portfolio, and market-data operations when configured with credentials.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact pyproject.toml reports 0.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
