## Description:

Retrieves public publisher headlines, searches, article text, live coverage, and section archives through the Crawlora API for source-specific news research.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crawlora-org](https://clawhub.ai/user/crawlora-org)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers and agents use this skill to find and read public news from specific publishers, retaining source links and timestamps for attribution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Requested news queries and article URLs are sent to a third-party service using a Crawlora API key.

Mitigation: Use only public-news queries and URLs; avoid secrets, private intranet URLs, unpublished documents, and sensitive investigative queries unless appropriate for the third-party API.

Risk: Bounded publisher feeds and challenged or partial articles can give an incomplete picture of coverage.

Mitigation: Preserve source URLs and timestamps, identify partial results, and do not present a single feed as exhaustive.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/crawlora-org/skills/news-media-research)
- [Publisher endpoint reference](reference/endpoints.md)
- [Crawlora](https://crawlora.net)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown research responses; retrieved publisher records are JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Include source URLs and publication times; results may be incomplete or partial.]

## Skill Version(s):

1.0.15 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
