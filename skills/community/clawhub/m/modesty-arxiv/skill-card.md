## Description:

Search, download, and summarize academic papers from arXiv. Built for AI/ML researchers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[modestyrichards](https://clawhub.ai/user/modestyrichards)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, students, content creators, and technical practitioners use this skill to search arXiv, inspect paper metadata, summarize abstracts, download PDFs, and manage a reading list for literature review workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Downloaded PDFs are written to local disk.

Mitigation: Use an isolated working directory and review the configured output path before downloading papers.

Risk: Optional MongoDB integration can store saved-paper history and reading statuses.

Mitigation: Enable MongoDB only when persistent research history is intended, and use an appropriate database with access controls.

Risk: Python dependencies are specified with broad minimum versions.

Mitigation: Install in an isolated Python environment and pin dependency versions for managed deployments.

## Reference(s):

- [Complete setup guide](https://skillboss.co/skill.md)
- [ClawHub skill page](https://clawhub.ai/modestyrichards/skills/modesty-arxiv)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Files, Guidance]

**Output Format:** [Markdown or JSON paper metadata, with optional PDF files written to disk.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Optional MongoDB reading-list state when configured.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
