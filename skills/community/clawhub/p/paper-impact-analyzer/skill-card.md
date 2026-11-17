## Description:

Analyze academic paper impact from an arXiv ID using arXiv, GitHub, OpenAlex, and Semantic Scholar, with graceful degradation when APIs are unavailable.

This skill is ready for commercial/non-commercial use.

## Publisher:

[haataa](https://clawhub.ai/user/haataa)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and literature-review agents use this skill to assess the external impact signals for one or more academic papers from arXiv IDs. It helps compare papers using publication metadata, venue signals, repository activity, citations, author metrics, and data completeness.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends paper IDs, titles, repository search terms, and first-author names to external academic and GitHub APIs.

Mitigation: Use it only for public or approved research topics, and run it in an environment where those external API calls are acceptable.

Risk: The security scan reports insecure external web request handling.

Mitigation: Review before installing, prefer an updated release that uses HTTPS for arXiv and normal TLS verification, and sandbox execution for sensitive workflows.

Risk: The skill requests broader local Read and Write authority than the analysis workflow appears to require.

Mitigation: Grant least-privilege tool access where possible and run without access to sensitive local files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/haataa/skills/paper-impact-analyzer)
- [arXiv API endpoint used by the skill](http://export.arxiv.org/api/query?id_list={arxiv_id})
- [GitHub repository API endpoint used by the skill](https://api.github.com/repos/{repo_path})
- [OpenAlex DOI lookup endpoint used by the skill](https://api.openalex.org/works/doi:{doi}?select=id,cited_by_count,publication_date)
- [Semantic Scholar paper endpoint used by the skill](https://api.semanticscholar.org/graph/v1/paper/ArXiv:{arxiv_id}?fields=citationCount,influentialCitationCount)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown impact report with tables, links, ratings, confidence, and source availability notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports single-paper and multi-paper analysis from arXiv IDs; output quality depends on availability and rate limits of external data sources.]

## Skill Version(s):

1.1.0 (source: ClawHub release evidence; artifact frontmatter and _meta.json report 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
