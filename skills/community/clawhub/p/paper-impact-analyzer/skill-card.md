## Description: <br>
Analyze academic paper impact from an arXiv ID using arXiv, GitHub, OpenAlex, and Semantic Scholar signals with graceful degradation when APIs are unavailable. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[haataa](https://clawhub.ai/user/haataa) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and literature-review agents use this skill to evaluate public arXiv papers with metadata, repository activity, citations, and author signals before deciding what to read or compare. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends arXiv IDs and related public paper metadata to arXiv, GitHub, OpenAlex, and Semantic Scholar. <br>
Mitigation: Use it for public academic paper checks and avoid confidential, embargoed, or sensitive research interests unless sharing this metadata is acceptable. <br>
Risk: The current script disables HTTPS certificate verification, which can allow network tampering with API responses. <br>
Mitigation: Treat results as advisory, run only in trusted environments, or update the script to enforce certificate verification before relying on the output. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/haataa/paper-impact-analyzer) <br>
- [README](artifact/skills/paper-impact-analyzer/README.md) <br>
- [Skill definition](artifact/skills/paper-impact-analyzer/SKILL.md) <br>
- [arXiv API](http://export.arxiv.org/api/query) <br>
- [GitHub REST API](https://api.github.com) <br>
- [OpenAlex API](https://api.openalex.org) <br>
- [Semantic Scholar Graph API](https://api.semanticscholar.org/graph/v1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown impact report with tables, source status, ratings, confidence, and data completeness.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Accepts one or more arXiv IDs; results depend on public arXiv, GitHub, OpenAlex, and Semantic Scholar API availability.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata; artifact frontmatter reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
