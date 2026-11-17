## Description:

AI-assisted Polymarket trading toolkit that helps agents scan prediction markets, evaluate probabilities, inspect order books, execute trades, monitor positions, track resolution, and backtest recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[donkeylmx](https://clawhub.ai/user/donkeylmx)

### License/Terms of Use:

MIT-0

## Use Case:

External developers, agents, and Polymarket users use this skill to analyze prediction markets, manage paper or live trading workflows, monitor positions, and review historical recommendation performance. Live-trading features require wallet credentials and should be used only with explicit financial-risk controls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Wallet-enabled workflows can place real Polymarket trades and cause financial loss, especially through no-confirmation automatic trading.

Mitigation: Use a dedicated low-balance wallet, keep dry-run mode enabled until tested, set strict trade limits, and avoid no-confirmation auto-trade mode unless the user accepts the loss risk.

Risk: Private keys or funding addresses may be exposed if pasted into chat or handled outside environment configuration.

Mitigation: Provide credentials only through environment files or variables, never through chat messages, logs, or generated reports.

Risk: Unpinned or stale dependencies in trading scripts can increase operational and supply-chain risk.

Mitigation: Review, update, or pin dependencies before use, and scan the installed artifact before enabling live-trading workflows.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/donkeylmx/skills/polymarket-trade-assistant)
- [ClawHub Homepage Metadata](https://clawhub.ai/skills/polymarket-trade-skills)
- [Polymarket CLOB Trading API Reference](artifact/api-trade-polymarket/references/clob-trading-api.md)
- [Environment Configuration Guide](artifact/api-trade-polymarket/references/env-setup.md)
- [Risk Controls Reference](artifact/danger-auto-trade-polymarket/references/risk-controls.md)
- [Market Pulse Analysis Framework](artifact/polymarket-market-pulse/references/analysis-framework.md)
- [Portfolio Schema](artifact/polymarket-paper-trading/references/portfolio-schema.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, JSON command results, code snippets, shell commands, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Some workflows read and write local portfolio, recommendation, and report files; trading workflows can call Polymarket APIs when configured with credentials.]

## Skill Version(s):

1.0.2 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
