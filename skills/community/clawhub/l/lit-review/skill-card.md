## Description: <br>
Automatically searches academic literature from Semantic Scholar, arXiv, and CrossRef, filters and clusters relevant papers, and generates a structured literature review draft. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[paudyyin](https://clawhub.ai/user/paudyyin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and research assistants use this agent to collect papers for a topic, rank and group the results, and draft a review with trends, themes, and references. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Research topics and queries are sent to public academic search services. <br>
Mitigation: Avoid submitting confidential, embargoed, or sensitive research topics unless the public services are approved for that use. <br>
Risk: Optional LLM polishing may send generated drafts and paper summaries to the configured model provider. <br>
Mitigation: Keep LLM polishing disabled for confidential work, or configure only a provider that is approved for the data being processed. <br>
Risk: Optional clustering and document-export dependencies can vary across environments. <br>
Mitigation: Use a virtual environment with pinned dependency versions for reproducible installs and reviews. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/paudyyin/lit-review) <br>
- [Semantic Scholar paper search API](https://api.semanticscholar.org/graph/v1/paper/search) <br>
- [arXiv API query endpoint](http://export.arxiv.org/api/query) <br>
- [CrossRef works API](https://api.crossref.org/works) <br>
- [Optional DeepSeek-compatible LLM endpoint](https://api.deepseek.com/v1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown literature review drafts, optional DOCX or plain text files, command-line guidance, and Python usage examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include paper metadata, topic clusters, trend summaries, and reference lists derived from public academic search results.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, skill.md frontmatter, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
