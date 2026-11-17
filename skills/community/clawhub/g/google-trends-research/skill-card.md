## Description:

Compares search interest, regional patterns, seasonality, and rising queries through Crawlora's Google Trends endpoints for topic-demand and keyword research.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crawlora-org](https://clawhub.ai/user/crawlora-org)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers and marketing teams use this skill to compare search interest and prepare topic-demand briefs with explicit query filters and relative-index caveats.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Trend queries and filters are sent to Crawlora; sensitive private topics could be disclosed.

Mitigation: Avoid sensitive private terms and filters; use the service only when sharing research inputs with Crawlora is acceptable.

Risk: The Crawlora API key is transmitted to the service.

Mitigation: Keep the key in the environment as instructed and review the helper's allowed routes before use.

Risk: Normalized trend scores and incomplete results can be mistaken for absolute demand or a complete comparison.

Mitigation: Compare terms within the same query, label scores as relative indices, and disclose missing data rather than treating it as zero.

## Reference(s):

- [Google Trends endpoint reference](reference/endpoints.md)
- [Google Trends data FAQ](https://support.google.com/trends/answer/4365533?hl=en)
- [ClawHub skill release](https://clawhub.ai/crawlora-org/skills/google-trends-research)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown brief or chart/table]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes terms, geography, period, search property, collection time, relative-index interpretation, and missing components when applicable.]

## Skill Version(s):

1.0.10 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
