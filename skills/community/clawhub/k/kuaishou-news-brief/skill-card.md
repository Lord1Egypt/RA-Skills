## Description:

Searches public Kuaishou videos, retrieves creators' public posts and video comments, and provides structured data for news briefs and audience analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators, marketing teams, and analysts use the skill to research public Kuaishou videos, track creator posts, and examine comments for trends, competitor monitoring, and briefings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Kuaishou keywords, profile or video URLs, and the GUAIKEI API token are sent to a third-party service.

Mitigation: Use only if that transfer is acceptable; keep the token secret and avoid sending sensitive search terms or links.

Risk: Locally saved results may include public comments and account or post data.

Mitigation: Restrict access to logs/ and delete retained results when no longer needed.

## Reference(s):

- [GUAIKEI service](https://www.guaikei.com)
- [Usage options](references/options.md)
- [Demand research workflow](references/demand-mining.md)

## Skill Output:

**Output Type(s):** [Structured data, Analysis, Guidance]

**Output Format:** [JSON results with optional text or Markdown summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Successful results are also saved locally under logs/.]

## Skill Version(s):

1.0.0 (source: release metadata, skill frontmatter, package.json and changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
