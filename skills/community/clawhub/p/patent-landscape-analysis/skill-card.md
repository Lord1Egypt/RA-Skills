## Description:

Maps a technology area using Crawlora Google Patents and USPTO searches, with documented query coverage, patent-family grouping, assignee normalization, dates, and classifications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crawlora-org](https://clawhub.ai/user/crawlora-org)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, patent analysts, and product teams use this skill to explore technology landscapes and compare patent portfolios through traceable searches, family grouping, and dated trends. It does not provide legal clearance conclusions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Patent search terms and identifiers are sent to Crawlora and may expose confidential invention details.

Mitigation: Obtain approval before searching confidential details and limit queries to the necessary scope.

Risk: A Crawlora API key is required for searches.

Mitigation: Keep the key scoped to Crawlora and handle it as a secret.

Risk: Incomplete search coverage or sampled families can lead to misleading conclusions about patent rights.

Mitigation: Document query scope, source dates, and missing evidence; treat findings as exploratory research, not legal advice or clearance.

## Reference(s):

- [Patent search endpoint reference](artifact/reference/endpoints.md)
- [Patent Landscape Analysis on ClawHub](https://clawhub.ai/crawlora-org/skills/patent-landscape-analysis)

## Skill Output:

**Output Type(s):** [Text, Markdown]

**Output Format:** [Markdown research report with tables and source links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes a query and coverage ledger, family and assignee map, topic matrix, dated trends, sample documents, and evidence gaps.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
