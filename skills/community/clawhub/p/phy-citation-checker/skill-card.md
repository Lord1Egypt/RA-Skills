## Description:

Verify academic citations against CrossRef, Semantic Scholar, and OpenAlex. Detects AI-hallucinated references, chimeric citations, and suspicious patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[phy041](https://clawhub.ai/user/phy041)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and technical writers use this skill to check BibTeX bibliographies before submitting papers, theses, reports, or CI/CD manuscript builds. It helps identify fabricated, chimeric, suspicious, or unresolved academic references.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bibliography titles and DOIs may be sent to CrossRef, Semantic Scholar, and OpenAlex during checks.

Mitigation: Review or redact .bib files before networked verification, especially for embargoed, confidential, or unpublished work.

## Reference(s):

- [Project homepage](https://github.com/PHY041/claude-skill-citation-checker)
- [ClawHub skill page](https://clawhub.ai/phy041/skills/phy-citation-checker)
- [Referenced arXiv paper](https://arxiv.org/abs/2501.04181)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with command examples and optional JSON citation reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May query citation titles and DOIs against CrossRef, Semantic Scholar, and OpenAlex.]

## Skill Version(s):

1.0.2 (source: ClawHub release metadata; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
