## Description:

PDF toolkit: extract, merge, split, compress, convert, watermark, and protect PDFs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[andreataide86](https://clawhub.ai/user/andreataide86)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to perform common PDF document operations through an agent, including extracting text, merging, splitting, compressing, converting, watermarking, and applying or removing password protection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs and runs PDF-processing Python dependencies, which introduces normal dependency-chain and local execution risk.

Mitigation: Install in an isolated environment and pin reviewed versions of pypdf, PyMuPDF, and Pillow before first use.

Risk: PDFs may contain sensitive content that local agents and installed libraries will process.

Mitigation: Avoid using sensitive PDFs unless the local agent environment and installed libraries are approved for that content.

Risk: PDF operations can overwrite or alter document outputs if paths are chosen carelessly.

Mitigation: Follow the skill guidance to avoid overwriting originals, append an output suffix by default, and ask before processing large or password-protected PDFs.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/andreataide86/skills/pdf-power)
- [Publisher Profile](https://clawhub.ai/user/andreataide86)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and generated PDF, text, or image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce derived PDF files, extracted text, converted page images, or extracted image folders; the skill instructs agents not to overwrite originals unless explicitly requested.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
