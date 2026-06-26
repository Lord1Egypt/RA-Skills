## Description: <br>
Autonomous Uniswap V3 monitoring on consensus-backed data with onchain provenance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[powerloom-bot](https://clawhub.ai/user/powerloom-bot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external DeFi operators use this skill to monitor Uniswap V3 swaps, detect whale activity, run token-flow and DeFi analyst recipes, and verify fetched data provenance on chain. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional wallet-funded setup can make an agent handle EVM private keys and irreversible on-chain payments. <br>
Mitigation: Prefer the free-key browser signup path. If wallet funding is used, use a low-balance burner wallet, run dry-run first, verify recipient, chain, token, and amount, and remove the private key after payment. <br>
Risk: Long-lived API keys, wallet keys, and webhook credentials can be exposed if pasted into chat or persisted in cron commands. <br>
Mitigation: Use a secret manager or protected environment injection instead of placing secrets in prompts, chat history, or inline scheduled commands. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/powerloom-bot/powerloom-bds-univ3) <br>
- [Powerloom BDS Metering](https://bds-metering.powerloom.io/metering) <br>
- [Hosted BDS MCP SSE](https://bds-mcp.powerloom.io/sse) <br>
- [Quickstart](references/01-quickstart.md) <br>
- [BDS MCP Tool Catalog](references/02-tool-catalog.md) <br>
- [Verification](references/03-verification.md) <br>
- [Credit Budget](references/04-credit-budget.md) <br>
- [Data Market Scope](references/05-data-market-scope.md) <br>
- [Troubleshooting](references/06-troubleshooting.md) <br>
- [Prompt Patterns](references/07-prompt-patterns.md) <br>
- [OpenClaw One-Shot Wallet-Funded Setup](references/08-openclaw-one-shot.md) <br>
- [OpenClaw One-Shot Free-Key Setup](references/09-openclaw-one-shot-free-key.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and recipe configuration; scripts produce text, JSON status, and alerts.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires POWERLOOM_API_KEY. Wallet-funded purchase scripts are optional and should be run with dry-run and explicit confirmation.] <br>

## Skill Version(s): <br>
0.2.6 (source: release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
