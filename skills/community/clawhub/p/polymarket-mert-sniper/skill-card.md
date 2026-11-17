## Description:

Near-expiry conviction trading on Polymarket that scans final-minute markets, filters for strongly skewed splits, and proposes or places bounded trades with dry-run as the default.

This skill is ready for commercial/non-commercial use.

## Publisher:

[simmer](https://clawhub.ai/user/simmer)

### License/Terms of Use:

MIT-0

## Use Case:

External users and trading-strategy developers use this skill to configure and run a near-expiry Polymarket scanning workflow with dry-run previews and optional live order placement through Simmer.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live mode can place real Polymarket trades, and on-chain orders cannot be recalled.

Mitigation: Keep dry-run enabled until configuration and wallet readiness are reviewed; use a dedicated low-balance wallet or API key for initial operation.

Risk: Managed ClawHub tunables advertise higher or different defaults than the README and Python defaults, changing trade-size and strategy exposure.

Mitigation: Verify the effective runtime values before enabling live or managed execution, especially max bet, expiry window, minimum split, and position sizing.

Risk: Portfolio and status commands can expose balances, open positions, and activity in terminal output or logs.

Mitigation: Avoid running status output in shared terminals or persistent logs, and limit API key access to the minimum needed for operation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/simmer/skills/polymarket-mert-sniper)
- [Strategy attribution thread](https://x.com/mert/status/2020216613279060433)
- [Simmer V2 migration guide](https://docs.simmer.markets/v2-migration)
- [Simmer API base](https://api.simmer.markets)
- [Polymarket CLOB API](https://clob.polymarket.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration values]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Dry-run status, market scan summaries, account status output, and live-trade execution guidance may be produced depending on command flags.]

## Skill Version(s):

1.3.6 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
