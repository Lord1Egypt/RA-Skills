## Description:

Jason Academic Writing runs an academic paper pipeline that gathers literature, drafts manuscript sections, performs citation and integrity checks, runs multi-role review, revises drafts, and records process summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ithacajason](https://clawhub.ai/user/ithacajason)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and academic writers use this skill to run an LLM-assisted workflow for literature collection, manuscript drafting, integrity checks, peer-review-style feedback, revision, and process reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Confidential or unpublished manuscripts may be sent to external services.

Mitigation: Use only with material approved for the configured OpenAI-compatible endpoint and public scholarly APIs; review OPENAI_API_KEY and OPENAI_BASE_URL settings before running.

Risk: Integrity reports may not prove that claims, statistics, methods, or citations were actually verified.

Mitigation: Treat integrity results as advisory and manually verify citations, methods, statistics, and evidence before submission or publication.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ithacajason/skills/jason-academic-writing)
- [Review Rubric](references/review_rubric.md)
- [Semantic Scholar API](https://api.semanticscholar.org)
- [Crossref Works API](https://api.crossref.org/works/)

## Skill Output:

**Output Type(s):** [markdown, json, shell commands, configuration, guidance]

**Output Format:** [Markdown manuscripts and summary reports, JSON evidence and review reports, and command-line guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes stage artifacts under an output working directory and requires configured OPENAI_API_KEY and OPENAI_BASE_URL values for LLM-backed stages.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
