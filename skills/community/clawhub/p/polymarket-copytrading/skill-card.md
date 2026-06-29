## Description: <br>
Mirror positions from top Polymarket traders with polling mode for portfolio-style copying and Reactor mode for event-driven real-time mirroring via Simmer's on-chain signal infrastructure. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[simmer](https://clawhub.ai/user/simmer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and their agents use this skill to configure and run Polymarket copytrading workflows, including dry-run checks, paper-mode trading, wallet-following scans, and Reactor-mode mirroring for eligible Simmer Pro users. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automated copytrading can place live trades with real funds when configured for live trading or Reactor mode. <br>
Mitigation: Start in dry-run or $SIM mode, use conservative position caps, and review venue, max_size, daily_cap, and watchlist settings before enabling live execution. <br>
Risk: A raw wallet private key used for external-wallet trading would expose funds if mishandled. <br>
Mitigation: Prefer managed wallets, or use a dedicated low-balance trading wallet when WALLET_PRIVATE_KEY is required. <br>
Risk: Reactor mode can execute live trades even when the normal dry-run default would otherwise apply. <br>
Mitigation: Treat Reactor setup as live automation, verify server-side Reactor configuration, and use the sim venue for paper trading. <br>
Risk: Strategy errors, market movement, signal lag, and misconfiguration can produce trading losses. <br>
Mitigation: Validate selected wallets and sizing in paper mode, keep per-position and daily caps low, and periodically review generated trade reports. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/simmer/skills/polymarket-copytrading) <br>
- [Simmer API](https://api.simmer.markets) <br>
- [Simmer Dashboard](https://simmer.markets/dashboard) <br>
- [Polymarket V2 Migration Guide](https://docs.simmer.markets/v2-migration) <br>
- [predicting.top](https://predicting.top) <br>
- [alphawhale.trade](https://alphawhale.trade) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, environment-variable configuration, API endpoints, and trade-status text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can produce dry-run summaries, account status, copytrading configuration, and live or simulated trade execution reports.] <br>

## Skill Version(s): <br>
1.12.1 (source: release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
