## Description:

Monitor RSS feeds for news that may move Polymarket markets, configure custom signal sources and keywords, and get article + market pairs with safeguard warnings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[simmer](https://clawhub.ai/user/simmer)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent developers use this skill to monitor configured RSS sources, match news against Polymarket markets, and pass article and market pairs with safeguards to an agent for review. It is intended for signal discovery and analysis, not autonomous trading.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The account-status script can read sensitive Simmer portfolio and position data.

Mitigation: Use a least-privilege Simmer API key where available, and avoid or remove scripts/status.py unless account reporting is intended.

Risk: Article and market pairs are signals, not validated trading recommendations, and RSS news may already be priced in.

Mitigation: Require agent or human review of the article, market resolution criteria, current price movement, and warnings before any trade is placed.

Risk: Real-money prediction market actions can produce irreversible losses if an agent acts on weak, stale, or misconfigured signals.

Mitigation: Run in paper mode first, configure trusted feeds and specific keywords, and keep any trading capability outside this read-only skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/simmer/skills/polymarket-signal-sniper)
- [Publisher profile](https://clawhub.ai/user/simmer)
- [Simmer dashboard](https://simmer.markets/dashboard)
- [Simmer Signal Sniper docs](https://docs.simmer.markets/skills/signal-sniper)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Plain text status output or a JSON object containing signals and an error field when run with --json.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Signals contain article, market, and warning fields; the skill does not place trades.]

## Skill Version(s):

2.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
