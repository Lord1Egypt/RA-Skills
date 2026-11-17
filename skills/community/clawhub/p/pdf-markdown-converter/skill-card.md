## Description:

Convert PDF documents to clean, well-formatted Markdown using the MinerU API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[veeicwgy](https://clawhub.ai/user/veeicwgy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, technical writers, and researchers use this skill to convert PDFs into Markdown for documentation, knowledge bases, blog publishing, and version-controlled research notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing mineru-open-api globally at the latest version can introduce unreviewed dependency changes.

Mitigation: Use a pinned or project-local mineru-open-api installation and avoid sudo during installation.

Risk: PDF contents may be sent through the MinerU API during conversion.

Mitigation: Convert only PDFs that are appropriate to process through the MinerU API.

Risk: Batch conversions can write many files to the selected output directory.

Mitigation: Review the output directory before running batch conversions.

## Reference(s):

- [PDF Markdown Converter on ClawHub](https://clawhub.ai/veeicwgy/skills/pdf-markdown-converter)
- [veeicwgy publisher profile](https://clawhub.ai/user/veeicwgy)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance, Files]

**Output Format:** [Markdown with inline shell commands and generated Markdown files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are written to a caller-selected or default conversion directory.]

## Skill Version(s):

0.2.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
