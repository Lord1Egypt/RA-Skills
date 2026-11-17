## Description:

Compare observed local business supply, categories, attributes, hours, and review-sample themes across defined areas using Crawlora's Google Maps dataset, live Google Maps, Apple Maps, and Yelp. Use for matched-area competitor landscapes and coverage comparisons; for user-supplied candidate-site screening with access and diligence gaps, use business-location-screening. Neither estimates demand, sales, or site viability.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crawlora-org](https://clawhub.ai/user/crawlora-org)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can compare observed business listings across consistently defined areas, including category mix, hours, attributes, and a disclosed sample of review themes. Use the results to describe source-specific coverage and observed differences, not demand or site viability.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends the API key you provide to Crawlora; install only if you trust Crawlora with that key.

Mitigation: Review the API access and key-handling behavior, and provide a key only when you trust Crawlora to receive it.

Risk: The security scan was partial because a local path-like reference could not be resolved, leaving related behavior unreviewed.

Mitigation: Resolve and inspect the referenced file and related behavior before relying on the benign scan verdict.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/crawlora-org/skills/local-competitive-landscape)
- [Endpoint reference](reference/endpoints.md)
- [Crawlora API key and service](https://crawlora.net?utm_source=github&utm_medium=referral&utm_campaign=crawlora-skills)

## Skill Output:

**Output Type(s):** [Analysis, Text, Markdown]

**Output Format:** [Markdown report with a coverage ledger, business matrix, and area comparison]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Preserves source-specific observations, unknowns, and disagreements; bounded search results do not establish local absence.]

## Skill Version(s):

1.0.7 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
