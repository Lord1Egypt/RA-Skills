## Description:

Converts PDF documents to LaTeX source code using MinerU AI extraction for academic papers, theses, and technical reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[decrystal](https://clawhub.ai/user/decrystal)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, academics, scientists, and developers use this skill to recover editable LaTeX from PDFs, including local files and PDF URLs. It is best suited for papers and technical documents with equations, tables, figures, multi-column layouts, or scientific notation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends PDFs to an external MinerU/OpenDataLab service through mineru-open-api.

Mitigation: Avoid submitting confidential PDFs unless organizational policy allows that service.

Risk: The skill depends on installing and running mineru-open-api from npm or Go package sources.

Mitigation: Install only from trusted package sources and prefer a pinned, reviewed CLI version in an isolated environment.

Risk: The workflow requires a MINERU_TOKEN credential.

Mitigation: Keep MINERU_TOKEN scoped and protected, and avoid exposing it in shared logs, shell history, or generated files.

## Reference(s):

- [MinerU homepage](https://mineru.net)
- [MinerU GitHub repository](https://github.com/opendatalab/MinerU)
- [MinerU token management](https://mineru.net/apiManage/token)
- [ClawHub skill page](https://clawhub.ai/decrystal/skills/pdf-to-latex-mineru)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration]

**Output Format:** [Markdown with inline bash commands and LaTeX-oriented guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides use of mineru-open-api to produce LaTeX output from PDF files or PDF URLs.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
