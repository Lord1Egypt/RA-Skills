## Description:

Automates academic literature searches across Semantic Scholar, arXiv, and CrossRef, filters and clusters results, and drafts structured literature reviews with optional LLM polishing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[paudyyin](https://clawhub.ai/user/paudyyin)

### License/Terms of Use:

MIT-0

## Use Case:

External researchers, students, and developers use this skill to gather academic papers for a topic, screen and group the results, and generate a structured literature review draft for further human review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional LLM writing can send an API key and research content to any configured endpoint.

Mitigation: Keep use_llm_for_writing disabled unless the configured provider is trusted, and avoid arbitrary llm_api_base values.

Risk: Research queries are sent to third-party academic services.

Mitigation: Avoid confidential or unpublished research topics, and prefer running the skill in a sandboxed virtual environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/paudyyin/skills/literature-review-automator)
- [Semantic Scholar Paper Search API](https://api.semanticscholar.org/graph/v1/paper/search)
- [arXiv API](http://export.arxiv.org/api/query)
- [CrossRef Works API](https://api.crossref.org/works)
- [DeepSeek API endpoint](https://api.deepseek.com/v1)

## Skill Output:

**Output Type(s):** [text, markdown, files, shell commands, configuration, guidance]

**Output Format:** [Markdown literature review documents, with optional DOCX or TXT output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses configurable publication-year range, maximum paper count, output format, optional human paper-list review, and optional LLM polishing disabled by default.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
