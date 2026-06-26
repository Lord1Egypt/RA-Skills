## Description: <br>
Provides a compatibility entry point for academic literature search across OpenAlex, Semantic Scholar, and arXiv with deduplication, citation-based ranking, and local caching. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jirboy](https://clawhub.ai/user/jirboy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, students, and developer agents use this skill to find relevant academic papers from multiple scholarly sources, remove duplicate records, and review ranked results with citation counts and identifiers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A crafted search input could cause unintended local shell command execution. <br>
Mitigation: Install only when inputs are trusted; replace shell command execution with argument-array process execution and validate query, numeric, and source fields before use. <br>
Risk: Search queries are sent to third-party academic services and results are cached locally. <br>
Mitigation: Avoid submitting confidential queries, disclose external API use to users, and provide cache controls or cache-clearing guidance. <br>


## Reference(s): <br>
- [Literature Search Pro release page](https://clawhub.ai/jirboy/literature-search-pro) <br>
- [OpenAlex Works API](https://api.openalex.org/works) <br>
- [Semantic Scholar Paper Search API](https://api.semanticscholar.org/graph/v1/paper/search) <br>
- [arXiv API query endpoint](http://export.arxiv.org/api/query) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON] <br>
**Output Format:** [JSON results plus Markdown-formatted search summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search results may include titles, authors, venues, years, abstracts, citation counts, DOI values, arXiv IDs, source labels, and cached timestamps.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
