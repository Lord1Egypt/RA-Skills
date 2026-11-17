## Description:

Literature review paper writing assistant that helps agents frame topics, search scholarly sources, validate DOI and arXiv identifiers, format citations, and draft structured Markdown literature reviews.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sherry-zh0u](https://clawhub.ai/user/sherry-zh0u)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and research teams use this skill to run systematic academic searches, validate paper identifiers, format citations, and assemble literature-review drafts for review articles, survey papers, thesis background chapters, or topic-based reference collection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms are sent to external scholarly APIs.

Mitigation: Use only queries and research topics that are acceptable to share with the configured academic services.

Risk: Sensitive unpublished research queries could be exposed when using the arXiv source before its endpoint is changed to HTTPS.

Mitigation: Avoid sensitive unpublished queries over the arXiv source and prefer HTTPS-backed sources for sensitive work.

Risk: Advertised advanced review features may be incomplete or may overstate the quality of generated review content.

Mitigation: Review generated literature reviews, citations, metadata conflicts, and source-quality tags before relying on the output.

## Reference(s):

- [Search Strategy Guide](references/search_strategy.md)
- [Literature Review API Reference](references/api_reference.md)
- [Semantic Scholar Graph API](https://api.semanticscholar.org/graph/v1/paper/search)
- [OpenAlex Works API](https://api.openalex.org/works)
- [CrossRef Works API](https://api.crossref.org/works)
- [PubMed E-utilities ESearch](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi)
- [PubMed E-utilities ESummary](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown, citation text, BibTeX, RIS, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can write formatted citation or review output to a user-specified file.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
