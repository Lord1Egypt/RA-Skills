## Description:

Trade on Polymarket via split + CLOB execution, browse markets, track positions with P&L, discover hedges via LLM analysis, and use automation tools for live portfolio tracking, auto-redeem, discipline scanning, and API bridge workflows on Polygon/Web3.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lmanchu](https://clawhub.ai/user/lmanchu)

### License/Terms of Use:

MIT

## Use Case:

External developers and trading-oriented agents use PolyClaw Pro to browse Polymarket markets, inspect wallet balances and positions, execute prediction-market trades on Polygon, and analyze hedge candidates. Operators should use reviewed transaction controls because the skill can automate trade, redeem, sell, and swap actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Wallet private keys can be used by trading, redemption, sell, and swap flows, including unattended automation.

Mitigation: Use a low-balance throwaway wallet, keep only funds you can afford to lose, and require manual approval for first-time or high-impact transaction paths.

Risk: Cron jobs and the API swap bridge can initiate unattended financial actions.

Mitigation: Do not enable cron jobs or the API swap bridge until every transaction path has explicit account checks, spending limits, and reviewed approval logic.

Risk: Hardcoded wallet addresses and incomplete account handling can cause actions or portfolio views to target the wrong account.

Mitigation: Remove hardcoded wallet addresses and derive all account state from the configured wallet before enabling trading automation.

Risk: Missing modules and unpinned dependencies reduce confidence in the reviewed transaction behavior.

Mitigation: Supply and audit all required modules, pin dependencies, and review the installed environment before running commands with funds.

## Reference(s):

- [PolyClaw Pro ClawHub listing](https://clawhub.ai/lmanchu/skills/polyclaw-pro)
- [PolyClaw README](artifact/README.md)
- [Polymarket](https://polymarket.com)
- [PolyClaw video explainer](https://www.youtube.com/watch?v=s_uP802NVTE)
- [Chainstack console](https://console.chainstack.com)
- [OpenRouter API keys](https://openrouter.ai/settings/keys)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands, configuration snippets, tables, and optional JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include live market, wallet, portfolio, risk, and transaction-status data from Polymarket, Polygon RPC, and configured API providers.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
