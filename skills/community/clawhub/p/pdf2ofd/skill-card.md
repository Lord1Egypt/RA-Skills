## Description:

Converts PDF documents (invoices, reports) to High-Fidelity OFD format with pixel-perfect precision.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xzw](https://clawhub.ai/user/xzw)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and document-workflow operators use this skill to convert selected PDFs, especially invoices and reports, into high-fidelity OFD files while preserving text placement, vector graphics, fonts, colors, images, and transparency.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: PDF parsing dependencies and large document handling can create operational risk.

Mitigation: Install and run the skill in an isolated environment, pin and review dependencies, and convert only PDFs intentionally selected by the user.

Risk: Exposing conversion as an upload-facing service can increase resource-exhaustion risk.

Mitigation: Add strict input size, page count, image, memory, disk, runtime, and concurrency limits before service deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xzw/skills/pdf2ofd)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with shell commands and generated OFD files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces an OFD output file from a selected PDF input path.]

## Skill Version(s):

1.0.2 (source: server release metadata; artifact frontmatter and package.json report 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
