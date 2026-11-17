## Description:

Assistance with writing literature reviews by searching for academic sources via Semantic Scholar, OpenAlex, Crossref and PubMed APIs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jirboy](https://clawhub.ai/user/jirboy)

### License/Terms of Use:

MIT-0

## Use Case:

External users and researchers use this skill to search academic databases, retrieve paper metadata and abstracts, compare source coverage, and draft literature review sections with citation-aware source details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Literature search terms are sent to Semantic Scholar, OpenAlex, Crossref, and PubMed, and optional email or API-key environment variables may identify the caller to those services.

Mitigation: Avoid sensitive search terms and set USER_EMAIL, CLAWDBOT_EMAIL, SEMANTIC_SCHOLAR_API_KEY, or OPENALEX_API_KEY only when that disclosure is intended.

Risk: Academic metadata and abstracts can vary by source, and Crossref results may lack abstracts.

Mitigation: Cross-check DOI or PMID records against source databases before using citations or conclusions in a final review.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jirboy/skills/literature-review-cn)
- [Semantic Scholar Graph API](https://api.semanticscholar.org/graph/v1)
- [OpenAlex API](https://api.openalex.org)
- [Crossref Works API](https://api.crossref.org/works)
- [PubMed E-utilities API](https://eutils.ncbi.nlm.nih.gov/entrez/eutils)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON search results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search results include paper identifiers, DOI or PMID values when available, titles, years, authors, abstracts, venues, citation counts, and source labels.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter reports 1.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
