## Description: <br>
Assists with literature reviews by searching Semantic Scholar, OpenAlex, Crossref, and PubMed for papers, DOI details, abstracts, and citation metadata used to draft cited review sections. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[weird-aftertaste](https://clawhub.ai/user/weird-aftertaste) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Researchers, students, and technical writers use this skill to find academic papers across major scholarly indexes, compare and deduplicate DOI-backed results, retrieve paper details, and organize source metadata into literature review drafts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Research queries, DOI lookups, contact email values, and optional API-key identifiers may be sent to third-party scholarly APIs. <br>
Mitigation: Use non-sensitive search terms where possible, set a non-sensitive contact email, and configure dedicated low-privilege API keys only when needed. <br>
Risk: Literature review drafts can reflect incomplete, stale, or incorrect metadata returned by external scholarly indexes. <br>
Mitigation: Verify important claims, citations, DOI values, and abstracts against the original papers or publisher records before relying on the review. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/weird-aftertaste/literature-review) <br>
- [Semantic Scholar API endpoint](https://api.semanticscholar.org/graph/v1) <br>
- [OpenAlex API endpoint](https://api.openalex.org) <br>
- [Crossref Works API endpoint](https://api.crossref.org/works) <br>
- [PubMed E-utilities endpoint](https://eutils.ncbi.nlm.nih.gov/entrez/eutils) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [JSON search results from helper commands plus Markdown guidance for synthesis and citation review.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search results include source identifiers, DOI or PMID when available, title, year, authors, abstract, venue, citation count when available, and source name.] <br>

## Skill Version(s): <br>
1.2.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
