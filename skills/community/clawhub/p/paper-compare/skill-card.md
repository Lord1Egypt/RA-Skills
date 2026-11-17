## Description:

Compare academic research papers side-by-side to identify similarities, differences, and research gaps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kexu9](https://clawhub.ai/user/kexu9)

### License/Terms of Use:


## Use Case:

External researchers, students, and developers use this skill to retrieve and compare one to five academic papers from DOIs, URLs, search queries, or PDFs, then receive a structured comparison, synthesis, and verdict.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs agents to save detailed paper-comparison history, including user goals and paper identifiers, which could expose sensitive research interests.

Mitigation: Make history storage opt-in, minimize saved fields, and provide clear retention and deletion controls before deployment.

Risk: Paper retrieval through web search, web fetch, and scholarly APIs may send paper choices, DOIs, URLs, or search terms to external services.

Mitigation: Review use with sensitive research topics and obtain user confirmation before sending confidential paper choices to external retrieval tools.

## Reference(s):

- [Paper Compare skill page](https://clawhub.ai/kexu9/skills/paper-compare)
- [Crossref Works API](https://api.crossref.org/works/{doi})
- [Semantic Scholar Paper API](https://api.semanticscholar.org/graph/v1/paper/{doi}?fields=citationCount)

## Skill Output:

**Output Type(s):** [Markdown, Analysis, Guidance]

**Output Format:** [Markdown with comparison tables, narrative summaries, quality scoring, and recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Compares one to five papers and may include research gaps, limitations, citation counts, code/data links, and a structured verdict.]

## Skill Version(s):

1.2.1 (source: frontmatter, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
