## Description:

Convert Markdown files to PDF, DOCX, or HTML with advanced formatting, Mermaid diagrams, custom fonts, and table of contents support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tuanpmt](https://clawhub.ai/user/tuanpmt)

### License/Terms of Use:


## Use Case:

Developers and document authors use this skill to convert Markdown documents or web articles into export formats such as PDF, DOCX, HTML, or clipboard-ready Markdown with formatting options.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installation steps build and globally link an unreviewed external MXE project from a hard-coded local path.

Mitigation: Inspect and trust the MXE source before installation, prefer a pinned local install, and avoid npm link or global installs unless that posture is acceptable.

Risk: URL inputs are treated as external network fetches.

Mitigation: Use trusted URLs and review downloaded content before converting or distributing generated documents.

## Reference(s):

- [Mxe Skill Page](https://clawhub.ai/tuanpmt/skills/mxe)
- [Artifact Skill Instructions](artifact/SKILL.md)
- [Artifact Package Metadata](artifact/package.json)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The referenced MXE tool can produce PDF, DOCX, HTML, or clipboard output; URL inputs should be treated as network fetches of external content.]

## Skill Version(s):

2.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
