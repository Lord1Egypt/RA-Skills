## Description:

Map artist discographies and comparable releases through Crawlora Spotify tools to create release-cohort or catalog-positioning briefs that preserve artist identities, release types, date precision, editions, and public-metric limits.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crawlora-org](https://clawhub.ai/user/crawlora-org)

### License/Terms of Use:

MIT-0

## Use Case:

Music analysts, artists, and their teams use this skill to compare public artist discographies and release cohorts, distinguishing primary releases, appearances, and editions while preserving source and date limitations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Crawlora receives API credentials and search queries; requests may consume credits.

Mitigation: Use a key scoped to Crawlora, monitor credit usage, and limit calls and pages to the requested scope.

Risk: Incomplete catalog coverage or snapshot popularity metrics may lead to misleading comparisons.

Mitigation: Attribute observations to their sources and dates, separate editions and appearances, and label coverage gaps and unverified trends.

## Reference(s):

- [Music Release Landscape on ClawHub](https://clawhub.ai/crawlora-org/skills/music-release-landscape)
- [Crawlora Spotify endpoint reference](reference/endpoints.md)

## Skill Output:

**Output Type(s):** [Markdown, Guidance]

**Output Format:** [Markdown brief with tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Sourced identity and date ledgers, a release matrix, positioning hypotheses, and unknowns.]

## Skill Version(s):

1.0.1 (source: server-resolved ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
