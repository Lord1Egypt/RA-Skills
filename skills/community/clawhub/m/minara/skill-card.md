## Description: <br>
Minara helps agents use the Minara CLI for crypto trading, wallet operations, perpetual futures, market discovery, AI analysis, x402 payments, and premium account workflows across EVM, Solana, and Hyperliquid. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lowesyang](https://clawhub.ai/user/lowesyang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use Minara to route crypto finance intents to the Minara CLI, check account and market data, and prepare or execute confirmed trades, transfers, deposits, withdrawals, subscriptions, and perpetual futures actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access authenticated crypto account data and help execute real trades, transfers, withdrawals, subscriptions, and perpetual futures actions. <br>
Mitigation: Install only for intended crypto account use, keep confirmation and Touch ID enabled, and do not use --yes for fund-moving commands. <br>
Risk: Setup guidance can persistently route future finance prompts through Minara by editing CLAUDE.md, AGENTS.md, or MEMORY.md. <br>
Mitigation: Review proposed workspace configuration edits before accepting them and decline broad persistent routing if it is not desired. <br>
Risk: Autopilot and perpetual futures workflows can materially change trading risk. <br>
Mitigation: Enable autopilot only with clear risk limits, and check autopilot status before placing manual perps orders. <br>


## Reference(s): <br>
- [Minara Homepage](https://minara.ai) <br>
- [ClawHub Release Page](https://clawhub.ai/lowesyang/minara) <br>
- [Workspace Integration](setup.md) <br>
- [Auth / Account / Config](references/auth.md) <br>
- [Balance / Assets](references/balance.md) <br>
- [AI Chat / Ask / Research](references/chat.md) <br>
- [Deposit / Receive](references/deposit.md) <br>
- [Market Discovery](references/discover.md) <br>
- [Minara Examples](references/examples.md) <br>
- [Spot Limit Orders](references/limit-order.md) <br>
- [Perps Autopilot / AI Analysis](references/perps-autopilot.md) <br>
- [Perps Positions / Close / Cancel / Leverage / Trades](references/perps-manage.md) <br>
- [Perps Order (Market / Limit)](references/perps-order.md) <br>
- [Perps Wallets / Deposit / Withdraw / Fund Records](references/perps-wallet.md) <br>
- [Premium / Subscription](references/premium.md) <br>
- [Swap (Buy / Sell)](references/swap.md) <br>
- [Transfer / Send / Pay](references/transfer.md) <br>
- [Withdraw](references/withdraw.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown responses with CLI command execution, structured confirmation summaries, and configuration instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Minara CLI access and authenticated account state for account-specific or fund-moving workflows.] <br>

## Skill Version(s): <br>
3.0.3 (source: server release metadata; artifact frontmatter says 3.0.2) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
