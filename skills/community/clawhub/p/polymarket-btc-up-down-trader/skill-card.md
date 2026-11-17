## Description:

Trade Polymarket BTC daily and weekly UP/DOWN markets with empirically-anchored exit discipline.

This skill is ready for commercial/non-commercial use.

## Publisher:

[simmer](https://clawhub.ai/user/simmer)

### License/Terms of Use:

MIT-0

## Use Case:

Traders and automation operators use this skill to scan Polymarket BTC daily and weekly direction markets, run dry-run checks, and optionally execute live entries and exits with configurable position and budget controls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live mode can place irreversible real-money Polymarket trades.

Mitigation: Start in dry run, use conservative position and daily-budget settings, and enable live mode only after reviewing the strategy and account risk.

Risk: Exporting WALLET_PRIVATE_KEY increases wallet custody exposure.

Mitigation: Avoid setting WALLET_PRIVATE_KEY unless external-wallet live trading is required; prefer managed-wallet or dry-run operation where appropriate.

Risk: Cron or looped execution can automate repeated trading decisions.

Mitigation: Review cron schedules and run monitor-only or dry-run checks before enabling unattended live execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/simmer/skills/polymarket-btc-up-down-trader)
- [Skill instructions](artifact/SKILL.md)
- [Disclaimer](artifact/DISCLAIMER.md)
- [Changelog](artifact/CHANGELOG.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and Python strategy execution output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May place live Polymarket trades only when explicitly run with live-trading configuration.]

## Skill Version(s):

1.2.5 (source: server release evidence, frontmatter, and changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
