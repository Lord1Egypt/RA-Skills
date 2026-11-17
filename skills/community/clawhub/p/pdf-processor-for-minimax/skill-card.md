## Description:

Uses MiniMax models to extract text and images from PDF files and analyze PDF document content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wanghanwanghan](https://clawhub.ai/user/wanghanwanghan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to build PDF processing workflows that extract text and embedded images, then send selected content to MiniMax models for summarization, image description, or custom document analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: PDF text and embedded images may be sent to MiniMax's external service.

Mitigation: Confirm the user or organization is allowed to send the target PDFs to MiniMax before processing, especially for confidential documents.

Risk: The skill recommends unpinned Python package installation commands.

Mitigation: Use an isolated environment and pin dependency versions where possible before deployment.

Risk: Large PDFs or image-heavy documents can increase API cost, latency, and rate-limit exposure.

Mitigation: Batch pages, resize large images before model calls, and add retry or delay handling for MiniMax API limits.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wanghanwanghan/skills/pdf-processor-for-minimax)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with Python and shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance includes dependency installation, MiniMax credential configuration, PDF extraction code, analysis workflow code, and operational cautions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
