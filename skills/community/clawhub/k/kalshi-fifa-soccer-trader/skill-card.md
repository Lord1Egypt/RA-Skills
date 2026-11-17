## Description:

Trade Kalshi soccer markets using EA FC OVR rating disparity and a bivariate Poisson model to find edge on match winner, total goals, and goal spread markets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bridgeaisocial](https://clawhub.ai/user/bridgeaisocial)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to evaluate and trade Kalshi soccer markets with EA FC OVR-based signals, bivariate Poisson scoring, market de-vigging, and configurable dry-run or live execution workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can execute live financial trades and uses wallet secrets.

Mitigation: Start in dry-run mode, keep SOLANA_PRIVATE_KEY unset until intentionally running live, use small position caps, and review every configured risk limit before funding a wallet.

Risk: Dependency and execution risk is elevated by the required simmer-sdk package.

Mitigation: Install in an isolated virtual environment and pin and verify simmer-sdk before use.

Risk: The SoFIFA scraper uses browser automation with stealth behavior.

Mitigation: Avoid the scraper unless needed, or run it in a containerized environment after accepting the browser automation risk.

Risk: Model outputs can be wrong because team aliases, lineup data, ratings, liquidity, and settlement rules may be incomplete or stale.

Mitigation: Review ambiguous team aliases, refresh ratings and lineup data, verify Kalshi settlement rules, and keep safeguards such as liquidity, slippage, and edge thresholds enabled.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bridgeaisocial/skills/kalshi-fifa-soccer-trader)
- [Disclaimer](DISCLAIMER.md)
- [DFlow Proof verification](https://dflow.net/proof)
- [Simmer Proof status API](https://api.simmer.markets/api/proof/status?wallet=YOUR_SOLANA_ADDRESS)
- [SoFIFA international teams](https://sofifa.com/teams?type=international&col=oa&sort=desc)
- [TheSportsDB API](https://www.thesportsdb.com/api/v1/json/3)
- [Wikipedia API](https://en.wikipedia.org/w/api.php)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and code or configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce dry-run analyses, command plans, edits to JSON ratings/configuration, and live-trading commands when explicitly enabled.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
