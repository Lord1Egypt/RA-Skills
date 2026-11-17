## Description:

Compress PDF files to a target size or by percentage, using a Ghostscript, pikepdf, and QPDF multi-stage pipeline.

This skill is ready for commercial/non-commercial use.

## Publisher:

[johnsonklose](https://clawhub.ai/user/johnsonklose)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and document-processing users use this skill to reduce PDF file sizes for sharing, storage, or upload limits while selecting either a target size or percentage reduction.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill automatically installs an unpinned Python package during normal use without a consent gate.

Mitigation: Use an isolated virtual environment or container, preinstall reviewed and pinned dependencies, and avoid automatic pip installation on systems with sensitive files or credentials.

Risk: PDF compression can degrade document image quality when aggressive quality settings are used.

Mitigation: Keep the default or high quality floor for print-sensitive documents and review compressed outputs before replacing originals.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/johnsonklose/skills/pdf-compress-tool)
- [Publisher profile](https://clawhub.ai/user/johnsonklose)
- [Ghostscript downloads](https://ghostscript.com/releases/gsdnld.html)
- [QPDF releases](https://github.com/qpdf/qpdf/releases)

## Skill Output:

**Output Type(s):** [text, shell commands, files, guidance]

**Output Format:** [Compressed PDF files with terminal status text and Markdown-style usage examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports single-file and batch PDF compression with target-size, percentage, and quality-floor options.]

## Skill Version(s):

1.0.2 (source: server release metadata; artifact frontmatter is 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
