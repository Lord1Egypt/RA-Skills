## Description: <br>
Assistance with writing literature reviews by searching for academic sources via Semantic Scholar, OpenAlex, Crossref and PubMed APIs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jirboy](https://clawhub.ai/user/jirboy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and research teams use this skill to find academic papers, retrieve DOI-based details, compare literature databases, and draft literature review sections with citation metadata. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries, optional API keys, and an optional email identifier may be sent to Semantic Scholar, OpenAlex, Crossref, or PubMed. <br>
Mitigation: Use non-confidential search terms, provide credentials only from trusted environments, and avoid unpublished sensitive research topics unless provider sharing is acceptable. <br>
Risk: Academic metadata, abstracts, citation counts, and generated review prose can be incomplete or stale. <br>
Mitigation: Cross-check DOI or PMID records and source publications before relying on citations or conclusions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jirboy/literature-review-cn) <br>
- [Semantic Scholar Graph API endpoint](https://api.semanticscholar.org/graph/v1) <br>
- [OpenAlex API endpoint](https://api.openalex.org) <br>
- [Crossref Works API endpoint](https://api.crossref.org/works) <br>
- [NCBI E-utilities endpoint](https://eutils.ncbi.nlm.nih.gov/entrez/eutils) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON search results from the helper script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search results include identifiers, DOI or PMID values when available, titles, years, authors, abstracts, venues, citation counts, and source labels.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
