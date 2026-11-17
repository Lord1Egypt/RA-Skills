## Description:

Compare reported institutional-manager 13F holdings through Crawlora live SEC and stored position tools, preserving filing dates, coverage, security classes, and value units.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crawlora-org](https://clawhub.ai/user/crawlora-org)

### License/Terms of Use:

MIT-0

## Use Case:

Research analysts and agents use this skill to compare reported institutional holdings, assess portfolio concentration and position overlap, and identify possible issuer holders from SEC 13F evidence. Results describe delayed reported positions, not current ownership or trades.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Crawlora API key or confidential query details could be exposed to unintended recipients.

Mitigation: Keep CRAWLORA_API_KEY private and send sensitive research queries to Crawlora only when intended.

Risk: Dataset searches can consume credits per returned record.

Mitigation: Limit searches and page sizes to the research scope and monitor credit usage.

Risk: Delayed, incomplete, or differently scaled 13F data can produce misleading ownership comparisons.

Mitigation: Report filing dates, completeness and raw value units; compare only matching securities and compatible reporting periods.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/crawlora-org/skills/institutional-ownership-research)
- [Crawlora endpoint reference](reference/endpoints.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Markdown research summary with comparable position rows and disclosed formulas]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes manager and filing identifiers, source dates and URLs, coverage and truncation notes, unit assumptions, and unresolved matches.]

## Skill Version(s):

1.0.2 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
