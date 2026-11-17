## Description:

Full-paper bilingual reader for Nature-series papers that converts a PDF or URL into structured, annotated Markdown with Chinese translation, figure grounding, source anchors, and section summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yang1bai](https://clawhub.ai/user/yang1bai)

### License/Terms of Use:

MIT-0

## Use Case:

External users, researchers, and developers use this skill to read, translate, summarize, and annotate scientific papers from a PDF path, DOI, arXiv ID, or URL into a bilingual Markdown study document.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may be used with papers from sources that the user is not authorized to access.

Mitigation: Use lawful paper sources such as publisher pages, arXiv, institutional access, or Unpaywall before generating the Markdown analysis.

Risk: The optional export behavior can save generated Markdown to an unintended path.

Mitigation: Confirm the export path with the user before writing any generated Markdown file.

Risk: Generated translations, summaries, figure notes, and source anchors can contain inaccuracies.

Mitigation: Review the generated Markdown against the source paper before using it for citation, publication, or research decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yang1bai/skills/nature-reader)
- [DOI resolver](https://doi.org/)
- [Unpaywall API](https://unpaywall.org/products/api)
- [arXiv](https://arxiv.org/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Files]

**Output Format:** [Structured Markdown bilingual paper analysis with summaries, translations, figure notes, citations, source anchors, and optional exported .md file.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Output options include full bilingual reading, summary-only reading, methods-focused reading, and export to a user-confirmed Markdown path.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
