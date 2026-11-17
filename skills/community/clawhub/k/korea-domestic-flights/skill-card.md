## Description:

Searches, compares, and monitors South Korea domestic flight fares with Korean airport names, natural-language dates, date-range scans, multi-destination comparison, and price alerts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[twbeatles](https://clawhub.ai/user/twbeatles)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel-planning agents use this skill to search South Korea domestic one-way and round-trip fares, compare destinations and date ranges, generate concise Korean fare briefings, and manage target-price watch rules.

### Deployment Geography for Use:

South Korea domestic air travel

## Known Risks and Mitigations:

Risk: The skill executes an unpinned local scraper dependency.

Mitigation: Install only when the local tmp/Scraping-flight-information repository is trusted, controlled, and pinned or verified before use.

Risk: Price-alert storage can be redirected to arbitrary user-supplied paths.

Mitigation: Keep the default alert-store path unless a reviewed workflow intentionally needs another file.

Risk: External provider site changes or browser environment failures can produce missing or stale fare results.

Mitigation: Run the included smoke or live dry-run checks before scheduled use and treat empty results as candidates for scraper maintenance review.

## Reference(s):

- [Domestic Airports Reference](references/domestic-airports.md)
- [Price Alerts Schema](references/price-alerts-schema.md)
- [Hybrid Smoke Fixtures](references/hybrid-smoke-fixtures.json)
- [ClawHub Skill Page](https://clawhub.ai/twbeatles/skills/korea-domestic-flights)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration]

**Output Format:** [Korean human-readable briefings, JSON search results, shell command invocations, and JSON price-alert rule files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include price calendars, recommendation reasons, search diagnostics, stdout alert messages, and dedupe metadata for saved watch rules.]

## Skill Version(s):

0.6.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
