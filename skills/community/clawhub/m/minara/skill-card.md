## Description:

Minara helps agents use the Minara CLI for crypto trading, wallet operations, perpetual futures, deposits, withdrawals, premium flows, x402 payments, and AI market analysis across EVM, Solana, and Hyperliquid.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lowesyang](https://clawhub.ai/user/lowesyang)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use Minara to route finance and crypto requests through the Minara CLI for live market discovery, AI analysis, wallet actions, swaps, transfers, deposits, withdrawals, limit orders, premium subscriptions, and Hyperliquid perpetual futures workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can broadly influence finance-related routing and agent behavior after workspace integration.

Mitigation: Review setup.md before installation and avoid automatic writes to global memory or routing files unless that persistent behavior is desired.

Risk: The skill relies on a globally installed, mutable Minara CLI for wallet and trading workflows.

Mitigation: Prefer a pinned and reviewed CLI version before use, and review update prompts before changing the installed CLI or skill version.

Risk: Credentials and wallet state may be exposed if MINARA_API_KEY or ~/.minara credentials are mishandled.

Mitigation: Keep MINARA_API_KEY and ~/.minara credentials out of chat, logs, screenshots, and shared files.

Risk: Trades, withdrawals, transfers, leverage changes, subscription changes, and autopilot actions can move funds or materially change financial exposure.

Mitigation: Require fresh user confirmation for every fund-moving or exposure-changing action, and do not use confirmation-skipping flags.

## Reference(s):

- [ClawHub Skill Listing](https://clawhub.ai/lowesyang/skills/minara)
- [Minara Homepage](https://minara.ai)
- [Setup](setup.md)
- [Auth / Account / Config](references/auth.md)
- [Agent Authentication Recovery](references/auth-recovery.md)
- [Interactive Commands - Agent Bypass Guide](references/interactive-commands.md)
- [Balance / Assets](references/balance.md)
- [AI Chat / Ask / Research](references/chat.md)
- [Market Discovery](references/discover.md)
- [Swap (Buy / Sell)](references/swap.md)
- [Transfer / Send / Pay](references/transfer.md)
- [Deposit / Receive](references/deposit.md)
- [Withdraw](references/withdraw.md)
- [Spot Limit Orders](references/limit-order.md)
- [Perps Order (Market / Limit)](references/perps-order.md)
- [Perps Positions / Close / Cancel / Leverage / Trades](references/perps-manage.md)
- [Perps Wallets / Deposit / Withdraw / Fund Records](references/perps-wallet.md)
- [Perps Autopilot / AI Analysis](references/perps-autopilot.md)
- [Premium / Subscription](references/premium.md)
- [Minara Examples](references/examples.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown responses with Minara CLI command execution, command-output summaries, and confirmation tables for fund-moving workflows.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the minara CLI and Minara credentials or MINARA_API_KEY. Fund-moving actions require fresh user confirmation and should not use confirmation-skipping flags.]

## Skill Version(s):

3.0.4 (source: SKILL.md frontmatter, target metadata, and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
