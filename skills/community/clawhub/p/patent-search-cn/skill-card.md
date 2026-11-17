## Description:

Searches and analyzes patent records worldwide, including prior art, similar patents, citations, legal status, patent documents, and portfolio trends.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ip930](https://clawhub.ai/user/ip930)

### License/Terms of Use:

MIT-0

## Use Case:

External users can search patent databases across China, the US, Europe, Japan, Korea, and WIPO for prior art, specific patent documents, legal status, citations, and organization or inventor portfolios. They can also refine search strategies and review patent statistics and trends.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API credentials may be exposed, and crafted patent identifiers may access files outside the cache folder.

Mitigation: Keep production keys out of chat, use a dedicated limited-credit key, and use a corrected release that restricts authenticated destinations and redirects and validates patent identifiers.

Risk: Patent queries may disclose confidential invention details to PatentMax.

Mitigation: Sanitize confidential details before submitting queries.

Risk: Timeouts and uncertain retries may lead to charges that local accounting misses.

Mitigation: Set a spending limit and verify charges after timeouts.

## Reference(s):

- [PatentMax API Platform](https://api.ip930.com/features/api-platform)
- [API Reference](artifact/references/api-reference.md)
- [Search Workflow](artifact/references/search-workflow.md)
- [Query Construction](artifact/references/query-construction.md)
- [Known Pitfalls](artifact/references/pitfalls.md)

## Skill Output:

**Output Type(s):** [Analysis, Text, Markdown, Files]

**Output Format:** [Text and Markdown search results, summaries, and analyses; patent files when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include patent records, citation and statistical summaries, legal-status details, and downloaded patent PDFs.]

## Skill Version(s):

1.1.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
