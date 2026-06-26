## Description: <br>
Literature review paper writing assistant that guides systematic academic search, DOI and arXiv ID validation, multi-format citation output, and structured Markdown review generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sherry-zh0u](https://clawhub.ai/user/sherry-zh0u) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, students, and developers use this skill to plan systematic literature searches, collect paper metadata from academic sources, validate identifiers, format citations, and draft a structured literature review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries, DOIs, arXiv IDs, and selected source requests may be sent to external academic metadata services. <br>
Mitigation: Avoid submitting sensitive or unpublished research topics, and review which sources are enabled before running searches. <br>
Risk: A Semantic Scholar API key can be used for higher rate limits. <br>
Mitigation: Keep real API keys in private local configuration or environment-based handling, and do not hardcode them into shared or version-controlled files. <br>
Risk: Preprints and cross-source metadata can be incomplete, provisional, or conflicting. <br>
Mitigation: Use the skill's validation and conflict-detection outputs, then manually verify important citations and claims before publication. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sherry-zh0u/literature-review-writing-assistant) <br>
- [Search Strategy Guide](references/search_strategy.md) <br>
- [Literature Review API Reference](references/api_reference.md) <br>
- [Semantic Scholar API keys](https://www.semanticscholar.org/api-keys) <br>
- [Semantic Scholar Graph API](https://api.semanticscholar.org/graph/v1/paper/search) <br>
- [OpenAlex Works API](https://api.openalex.org/works) <br>
- [Crossref Works API](https://api.crossref.org/works) <br>
- [PubMed E-utilities Search API](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi) <br>
- [PubMed E-utilities Summary API](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with citations, shell command examples, and optional BibTeX, RIS, APA, MLA, IEEE, or JSON-like paper metadata.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call external academic metadata services and may use an optional Semantic Scholar API key.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
