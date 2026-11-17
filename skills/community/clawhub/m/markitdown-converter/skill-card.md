## Description:

Converts PDFs, Office documents, HTML, text, and other supported files to Markdown using Microsoft MarkItDown, with batch conversion and best-effort image extraction helper scripts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wang-junjian](https://clawhub.ai/user/wang-junjian)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and document-processing users use this skill to convert individual files or folders of supported documents into Markdown and to attempt image extraction from documents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installation guidance includes an option that uses --break-system-packages and dependency versions are not pinned.

Mitigation: Install in a dedicated virtual environment, prefer pinned dependency versions, and avoid --break-system-packages.

Risk: Format preservation and image extraction may not be complete for every supported document type.

Mitigation: Treat conversion and image extraction results as best-effort and review generated Markdown or extracted assets before relying on them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wang-junjian/skills/markitdown-converter)

## Skill Output:

**Output Type(s):** [Markdown, Files, Shell commands, Guidance]

**Output Format:** [Markdown files and concise shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Processes only the files or directories the user points it at; conversion fidelity and image extraction are best-effort.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
