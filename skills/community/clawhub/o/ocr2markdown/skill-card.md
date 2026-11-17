## Description:

Document OCR and parsing skill that converts local PDF files and images to Markdown on a remote Modal L4 GPU while preserving layout, tables, formulas, and OCR text.

This skill is ready for commercial/non-commercial use.

## Publisher:

[speech2srt](https://clawhub.ai/user/speech2srt)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and document-processing users use this skill to upload PDFs to a Modal-backed OCR pipeline, run MinerU parsing, and retrieve Markdown plus extracted images and auxiliary layout outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Documents are uploaded to persistent Modal storage.

Mitigation: Use only documents suitable for upload to Modal, keep OCR work in isolated volumes, and delete remote data when processing is complete.

Risk: Unsafe task-name handling can access or write outside the intended job folder.

Mitigation: Use simple slugs containing only letters, numbers, and dashes, and validate slugs before running the workflow.

Risk: Shared volumes can mix unrelated OCR jobs or data.

Mitigation: Avoid sharing volumes with unrelated jobs and document retention and cleanup expectations before deployment.

Risk: Unpinned runtime dependencies can change OCR behavior or risk profile.

Mitigation: Pin dependencies and review the build image before treating the skill as low risk.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/speech2srt/skills/ocr2markdown)
- [Publisher profile](https://clawhub.ai/user/speech2srt)

## Skill Output:

**Output Type(s):** [Markdown, Files, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown files with extracted image folders, auxiliary PDF/JSON files, and concise shell-command workflow guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are stored under a slug-specific output directory and already-processed PDFs are skipped on rerun.]

## Skill Version(s):

v1.0.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
