## Description:

Searches academic papers using the Semantic Scholar API and returns paper metadata including citations, abstracts, authors, and open-access PDF links when available.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhoujc11](https://clawhub.ai/user/zhoujc11)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and agents use this skill to search academic literature, retrieve paper metadata, inspect citations and abstracts, and get open-access PDF links when available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Academic search terms and paper IDs are sent to Semantic Scholar.

Mitigation: Do not use confidential project names, sensitive research topics, or private identifiers as queries unless third-party API sharing is acceptable.

Risk: Semantic Scholar rate limits can interrupt searches.

Mitigation: Retry after a short delay or reduce request frequency when the API returns rate-limit errors.

## Reference(s):

- [Semantic Scholar](https://www.semanticscholar.org)
- [Semantic Scholar API](https://api.semanticscholar.org)
- [Semantic Scholar API Product Page](https://www.semanticscholar.org/product/api)
- [API Reference](references/API.md)
- [ClawHub Skill Page](https://clawhub.ai/zhoujc11/skills/google-scholar-search)

## Skill Output:

**Output Type(s):** [text, json, shell commands, guidance]

**Output Format:** [Plain text or JSON paper-search results, with Markdown usage examples in the skill documentation.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results may include paper titles, authors, years, venues, citation counts, abstracts, Semantic Scholar URLs, open-access PDF links, and paper IDs.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
