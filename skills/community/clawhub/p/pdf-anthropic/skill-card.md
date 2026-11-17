## Description:

Provides guidance, code examples, shell commands, and helper scripts for reading, creating, modifying, filling, encrypting, decrypting, and OCR-processing PDF files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pupuking723](https://clawhub.ai/user/pupuking723)

### License/Terms of Use:

Proprietary Anthropic Terms

## Use Case:

Developers and agents use this skill to choose Python libraries, JavaScript libraries, command-line tools, and local helper scripts for common PDF operations including text extraction, table extraction, document assembly, form filling, OCR, encryption, and image extraction.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: PDF edits, repair operations, and generated outputs can overwrite or alter important documents.

Mitigation: Run workflows on copies of important PDFs and keep backups before repair, form-filling, encryption, or conversion tasks.

Risk: Password removal and decrypted PDF outputs can expose sensitive document contents.

Mitigation: Create decrypted copies only when needed, store them carefully, and delete temporary outputs when the task is complete.

Risk: OCR workflows can require additional local dependencies that are not pinned by the skill artifact.

Mitigation: Use a virtual environment with pinned dependencies before installing OCR-related packages.

## Reference(s):

- [PDF Form Filling Workflow](artifact/forms.md)
- [PDF Processing Advanced Reference](artifact/reference.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration, files]

**Output Format:** [Markdown guidance with code blocks, shell commands, and JSON file schemas]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local PDF, image, text, JSON, or spreadsheet files when used with user-provided documents.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
