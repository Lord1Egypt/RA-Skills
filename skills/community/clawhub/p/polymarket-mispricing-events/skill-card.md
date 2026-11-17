## Description:

Detects Polymarket mispricings by comparing prices with Kalshi and Manifold consensus probabilities and can place Simmer trades sized with a quarter-Kelly rule.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mibayy](https://clawhub.ai/user/mibayy)

### License/Terms of Use:

MIT-0

## Use Case:

External users running ClawHub automations use this skill to scan active prediction markets for cross-platform price gaps and, with a Simmer API key, place scheduled Polymarket trades in sim or live mode.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automated trading authority can place scheduled trades when live credentials are used.

Mitigation: Start with the sim venue and avoid live credentials until position limits, portfolio checks, and operational controls have been reviewed.

Risk: Fuzzy cross-platform market matching can produce false positives or compare markets with different resolution criteria.

Mitigation: Require high-confidence matches, review thresholds against representative markets, and keep position sizes conservative.

Risk: Portfolio and market-context checks may fail open if upstream calls are unavailable.

Mitigation: Make portfolio and context validation fail closed before deploying with live trading authority.

Risk: Unpinned Python dependencies can change behavior over time.

Mitigation: Pin and review dependency versions before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mibayy/skills/polymarket-mispricing-events)
- [Polymarket Gamma API endpoint](https://gamma-api.polymarket.com)
- [Polymarket CLOB API endpoint](https://clob.polymarket.com)
- [Kalshi trade API endpoint](https://api.elections.kalshi.com/trade-api/v2)
- [Manifold markets API endpoint](https://api.manifold.markets/v0)

## Skill Output:

**Output Type(s):** [API Calls, Text, Configuration]

**Output Format:** [Scheduled Python automation with log output and Simmer trade requests]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SIMMER_API_KEY; default venue is sim; live mode can place real trades when configured.]

## Skill Version(s):

1.0.0 (source: frontmatter, clawhub.json, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
