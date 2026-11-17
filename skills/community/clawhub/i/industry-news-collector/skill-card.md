## Description:

Collects, validates, ranks, and summarizes recent news for a requested industry, with Chinese-language summaries and source links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alpzhang](https://clawhub.ai/user/alpzhang)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external users, and analysts use this skill to gather recent industry news across product, business, research, policy, and market dimensions, then receive a heat-ranked Chinese summary with links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search-heavy workflows can consume time and tool quota or return uneven coverage.

Mitigation: Set a clear industry, region, and time window before running the skill; review the coverage statistics in the final digest.

Risk: The skill favors Chinese-language sources and summaries, which may miss or down-rank non-Chinese coverage.

Mitigation: Ask explicitly for another language, market, or source mix when the target industry is not China-focused.

Risk: Public-web news can be duplicated, stale, paywalled, or sourced from outlets with varying reliability.

Mitigation: Use the skill's cross-source validation, deduplication, HTTPS preference, and source links to review high-impact items before acting on them.

## Reference(s):

- [Recommended Industry News Sources](references/sources.md)
- [ClawHub skill page](https://clawhub.ai/alpzhang/skills/industry-news-collector)
- [ClawHub publisher profile](https://clawhub.ai/user/alpzhang)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown news digest in Chinese with ranked items, short summaries, source links, and collection statistics.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Typically 15-25 deduplicated news items sorted by heat after at least eight searches across the documented dimensions.]

## Skill Version(s):

1.0.0 (source: server release evidence and _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
