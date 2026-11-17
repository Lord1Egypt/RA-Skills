## Description:

PDF parsing tool for AI/RAG that converts PDF files to Markdown, JSON, HTML, text, rebuilt PDF, and image-aware Markdown with layout preservation, bounding boxes, and image extraction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wtjjacobj](https://clawhub.ai/user/wtjjacobj)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to extract content from PDFs for AI processing, RAG pipelines, and document analysis. It helps agents propose opendataloader-pdf CLI commands for conversion, page selection, image extraction, sanitization, and batch processing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing or running an unreviewed package version could execute unexpected local code.

Mitigation: Install from a trusted package source and pin a reviewed version before using the skill in production workflows.

Risk: Converted PDFs and extracted images may expose sensitive document content in local output directories.

Mitigation: Write outputs only to access-controlled directories, use stdout or sanitization options when appropriate, and avoid shared or world-readable paths.

Risk: PDF conversion relies on a Java runtime and spawns a JVM process for conversion, which can affect runtime behavior and performance.

Mitigation: Verify Java availability in the deployment environment and prefer batch conversion for multiple files.

## Reference(s):

- [OpenDataLoader PDF project homepage](https://github.com/opendataloader-project/opendataloader-pdf)
- [ClawHub skill page](https://clawhub.ai/wtjjacobj/skills/opendataloader-pdf-wuxie)
- [Test script](references/test_script.sh)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, HTML, Shell commands, Guidance]

**Output Format:** [Markdown guidance with inline shell commands; converted PDF outputs may be Markdown, JSON, HTML, text, PDF, or image files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports page ranges, image extraction, structure-tree parsing, table-detection modes, reading-order options, optional sanitization, stdout output, and batch conversion.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
