## Description: <br>
Compare academic research papers side-by-side to identify similarities, differences, and research gaps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[KeXu9](https://clawhub.ai/user/KeXu9) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Researchers, students, and technical readers use this skill to compare one to five academic papers from DOIs, URLs, search queries, or PDF files. It helps identify methodology differences, results, limitations, research gaps, and actionable recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may save paper-comparison history, which can expose confidential research context or sensitive literature-review strategy. <br>
Mitigation: For confidential or unpublished research, instruct the agent not to save or use history and avoid submitting material that should not be retained. <br>


## Reference(s): <br>
- [Paper Compare on ClawHub](https://clawhub.ai/KeXu9/paper-compare) <br>
- [Crossref Works API](https://api.crossref.org/works/{doi}) <br>
- [Semantic Scholar Graph API citation count endpoint](https://api.semanticscholar.org/graph/v1/paper/{doi}?fields=citationCount) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown comparison table with narrative analysis, quality assessment, decision matrix, and recommendation.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Compares one to five papers and may save comparison history unless instructed otherwise.] <br>

## Skill Version(s): <br>
1.2.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
