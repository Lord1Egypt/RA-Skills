## Description:

Literature Search Pro provides a compatibility layer for academic literature search across OpenAlex, Semantic Scholar, and arXiv with deduplication, citation-based sorting, and caching.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jirboy](https://clawhub.ai/user/jirboy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and agent users can use this skill to retrieve academic literature from multiple scholarly indexes and receive deduplicated, citation-ranked paper summaries. It also preserves legacy scholar usage while directing users toward the unified search scholar entry point.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Node entry point can turn search inputs into shell commands, creating an execution risk if exposed to untrusted inputs.

Mitigation: Review before installing or running; replace shell command construction with argument-array process execution and validate runtime inputs before exposing the skill to untrusted users.

Risk: The skill depends on external academic APIs and a Python requests runtime dependency.

Mitigation: Use HTTPS endpoints where available, pin the Python requests dependency, and account for third-party API availability and rate limits during deployment.

## Reference(s):

- [Literature Search Pro on ClawHub](https://clawhub.ai/jirboy/skills/literature-search-pro)
- [OpenAlex Works API](https://api.openalex.org/works)
- [Semantic Scholar Paper Search API](https://api.semanticscholar.org/graph/v1/paper/search)
- [arXiv API](http://export.arxiv.org/api/query)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON]

**Output Format:** [JSON object with a Markdown-formatted results message]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results include paper metadata such as title, authors, year, venue, citation count, DOI, arXiv ID, abstract, source, and cache timestamp when returned by the Python searcher.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
