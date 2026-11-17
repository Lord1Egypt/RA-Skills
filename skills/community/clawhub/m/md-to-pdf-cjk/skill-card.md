## Description:

Convert Markdown files to professional PDF documents with full CJK (Chinese/Japanese/Korean) support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zacjiang](https://clawhub.ai/user/zacjiang)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to convert Markdown documents into PDF files with CJK text support for reports, documentation, invoices, proposals, contracts, and batch conversion workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unpinned ReportLab installation may change behavior across environments.

Mitigation: Use a virtual environment and pin the ReportLab version before installing.

Risk: Optional sudo font installation modifies the host system.

Mitigation: Run package-manager font installation only when CJK fonts are required and OS package sources are trusted.

Risk: The converter reads and writes local file paths supplied at runtime.

Mitigation: Treat it as a local file tool and review input and output paths before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zacjiang/skills/md-to-pdf-cjk)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with shell commands and generated PDF file output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads a local Markdown input path and writes a local PDF output path.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
