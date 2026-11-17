## Description:

Converts Markdown files to Word documents and Word documents to Markdown while preserving common document structure where possible.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huangesun](https://clawhub.ai/user/huangesun)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, employees, and external users use this skill to convert .md and .docx files individually or in batches and receive the converted file path or download location.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release evidence flags unrelated persistent memory access for a document conversion workflow.

Mitigation: Install without persistent memory permissions where possible and avoid processing sensitive documents unless the runtime policy prevents unnecessary retention.

Risk: Large or media-heavy DOCX files may create memory, CPU, or disk pressure during image extraction.

Mitigation: Use trusted documents in a sandboxed environment with file size, memory, CPU, and disk limits.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/huangesun/skills/md-docx)
- [Publisher profile](https://clawhub.ai/user/huangesun)

## Skill Output:

**Output Type(s):** [text, markdown, files, configuration, guidance]

**Output Format:** [Markdown or text response with generated .md or .docx file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates timestamped outputs in a converted directory by default; output directory, conversion mode, and image preservation can be configured.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
