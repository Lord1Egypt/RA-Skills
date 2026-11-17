## Description:

Collects and validates Iranian currency, gold, and cryptocurrency market data for sourced snapshots and neutral Persian-language reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ehsanghaffar](https://clawhub.ai/user/ehsanghaffar)

### License/Terms of Use:

MIT-0

## Use Case:

Analysts and other users monitoring Iranian markets use this skill to collect sourced prices, identify unavailable or stale data, and prepare neutral Persian market summaries without investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live third-party quotes can be stale, unavailable, or inconsistent, leading to misleading financial summaries.

Mitigation: Check timestamps and source attribution, retain missing values as missing, and independently verify prices before making financial decisions.

Risk: Live collection contacts public websites and can write dated JSON snapshots to local storage.

Mitigation: Use --stdout-only when file persistence is unnecessary; otherwise choose a restricted output directory and review network access.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/ehsanghaffar/skills/iran-finance-markets-monitor)
- [Market data sources and validation guidance](references/market-data-sources.md)

## Skill Output:

**Output Type(s):** [Text, Files]

**Output Format:** [Persian Markdown report and structured JSON snapshot]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Snapshots include source attribution, Tehran timestamps, and explicit errors or warnings for missing data; dated JSON files are optional.]

## Skill Version(s):

0.1.2 (source: server-resolved ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
