## Description:

Guides agents through Google Search Console analysis, including search performance, indexing, sitemaps, Core Web Vitals, enhancements, and Search Console API use.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kostja94](https://clawhub.ai/user/kostja94)

### License/Terms of Use:

MIT-0

## Use Case:

External users, SEO analysts, and developers use this skill to interpret Google Search Console reports, investigate traffic or indexing changes, and turn performance data into prioritized SEO actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may lead an agent to analyze Google Search Console exports or API data that can include sensitive site performance details.

Mitigation: Provide only Search Console properties, exports, and reports that are intended for the analysis task.

Risk: SEO conclusions can be misleading if they are based on incomplete date ranges, default top-row limits, or uncorrelated release events.

Mitigation: Review date ranges, pagination, exported metrics, and relevant release or site-change history before acting on recommendations.

## Reference(s):

- [Search Console API](https://developers.google.com/webmaster-tools/about)
- [searchanalytics.query](https://developers.google.com/webmaster-tools/v1/how-tos/search_analytics)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown analysis with summaries, metrics, CTR findings, title and meta opportunities, action items, correlation notes, and next steps.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use user-provided or user-authorized Google Search Console exports or API data; no executable files are included in the artifact.]

## Skill Version(s):

1.5.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
