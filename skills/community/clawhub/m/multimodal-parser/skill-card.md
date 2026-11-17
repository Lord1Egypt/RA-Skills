## Description:

Unified multi-modal content parser for images, PDF, DOCX, audio, auto OCR/transcription, output structured text for LLM processing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ayalili](https://clawhub.ai/user/ayalili)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill as a local parsing layer to extract text from images, PDFs, Word documents, and audio for document question answering, knowledge-base preparation, OCR, transcription, and batch processing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill processes local files and downstream workflows may handle sensitive document, image, or audio content.

Mitigation: Avoid sensitive inputs unless retention and sharing behavior are understood, and restrict file access to only the inputs intended for parsing.

Risk: The skill relies on local parser tools and installable dependencies for OCR, document parsing, and transcription.

Mitigation: Install dependencies in an isolated environment with pinned versions before using the skill for normal workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ayalili/skills/multimodal-parser)
- [Zod Deno module](https://deno.land/x/zod@v3.22.4/mod.ts)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, guidance]

**Output Format:** [Plain text, Markdown, or structured JSON-like object returned with status and metadata.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns success status, detected file type, output format, parsed content, and parser metadata; error responses may include dependency installation guidance.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
