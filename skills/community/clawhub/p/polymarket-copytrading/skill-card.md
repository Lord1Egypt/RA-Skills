## Description:

Mirror positions from top Polymarket traders. Polling mode (free) for portfolio-style copying, Reactor mode (Pro) for event-driven real-time mirroring via Simmer's on-chain signal infrastructure.

This skill is ready for commercial/non-commercial use.

## Publisher:

[simmer](https://clawhub.ai/user/simmer)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to inspect Polymarket trader positions, configure whale wallets to follow, run dry-run or paper copytrading checks, and optionally execute live mirrored trades with configured caps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can place real-money trades when live mode and credentials are configured.

Mitigation: Use dry-run or $SIM paper mode first, keep per-position and per-run caps small, and review proposed trades before scaling to real USDC.

Risk: Automatic venue routing can convert above-cap simulated Reactor signals to Polymarket orders.

Mitigation: Set COPYTRADING_FORCE_SIMMER_VENUE=true when simulated-only execution is required.

Risk: Unattended live runs can continue acting on new whale signals without active review.

Mitigation: Avoid cron, loop, or nohup live execution until behavior, wallet setup, and caps have been reviewed.

Risk: External-wallet trading depends on WALLET_PRIVATE_KEY, which is highly sensitive.

Mitigation: Store the private key only in a protected environment and avoid exposing it in logs, prompts, shell history, or shared configuration.

Risk: Sell behavior and rebalance options can close positions as well as buy mirrored positions.

Mitigation: Review sell-related flags and defaults before live use, and confirm whether buy-only, whale-exit, or full-rebalance behavior is intended.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/simmer/skills/polymarket-copytrading)
- [Simmer API](https://api.simmer.markets)
- [Simmer dashboard](https://simmer.markets/dashboard)
- [Simmer V2 migration guide](https://docs.simmer.markets/v2-migration)
- [predicting.top](https://predicting.top)
- [alphawhale.trade](https://alphawhale.trade)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and terminal-oriented status summaries with inline shell commands and configuration values]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May run dry-run, paper, or live trading commands depending on user configuration; live trading requires Simmer credentials and, for external wallets, a wallet private key.]

## Skill Version(s):

1.12.4 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
