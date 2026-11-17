## Description:

Provides Chinese-language guidance and scripts for adding text or image watermarks to local PDF files, with batch-processing support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pwcy1978-boop](https://clawhub.ai/user/pwcy1978-boop)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and document operators use this skill to add configurable text or image watermarks to local PDF files, including Chinese text and batch processing. Do not rely on the advertised watermark-removal path to redact or sanitize documents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release advertises PDF watermark removal, but the shipped removal function only copies the original file unchanged.

Mitigation: Use the skill for local watermark addition only; do not use it to remove watermarks, redact identifying marks, or sanitize documents.

Risk: Batch processing can write many output PDFs and may overwrite or misplace files if paths are chosen carelessly.

Mitigation: Use explicit input and output paths, process copies where practical, and keep backups before running batch jobs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pwcy1978-boop/skills/pdf-watermark-chinese)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Files]

**Output Format:** [Markdown guidance with Python snippets and command-line instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or copy local PDF files when the bundled scripts are run.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
