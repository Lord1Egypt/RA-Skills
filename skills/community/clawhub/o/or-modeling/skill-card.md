## Description:

Helps agents translate real-world operations research problems into mathematical optimization models, validate assumptions, search academic literature when needed, and produce LaTeX formulations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[go-own-way](https://clawhub.ai/user/go-own-way)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and operations researchers use this skill to turn business or engineering optimization scenarios into model assumptions, objectives, constraints, solver guidance, self-check reports, and LaTeX model writeups.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Paper searches send search keywords to OpenAlex and Semantic Scholar.

Mitigation: Avoid including confidential business details, personal data, or proprietary model inputs in search terms unless sharing them with those services is acceptable.

## Reference(s):

- [Operations Research Problem Reference](references/or-problems.md)
- [OpenAlex Works API](https://api.openalex.org/works)
- [Semantic Scholar Paper Search API](https://api.semanticscholar.org/graph/v1/paper/search)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance]

**Output Format:** [Markdown with LaTeX model blocks and optional shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include literature-search summaries sourced from OpenAlex and Semantic Scholar when paper_search.py is used.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
