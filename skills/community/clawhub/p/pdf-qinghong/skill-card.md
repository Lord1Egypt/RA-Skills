## Description:

Helps agents read, extract, transform, create, secure, OCR, and fill PDF files using Python libraries and command-line tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qinghong268](https://clawhub.ai/user/qinghong268)

### License/Terms of Use:

Proprietary

## Use Case:

Developers and agent users use this skill to perform common PDF workflows such as text and table extraction, document merging or splitting, form filling, OCR, image extraction, encryption, and PDF generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: PDF workflows can read sensitive documents and create local derivative files such as images, text extracts, filled PDFs, and form-data JSON.

Mitigation: Use only PDFs the user is authorized to process, keep originals separate from generated outputs, and delete temporary files containing sensitive data when work is complete.

Risk: PDF commands and scripts may overwrite files or depend on locally installed PDF libraries and utilities.

Mitigation: Review proposed commands before execution, avoid overwriting original PDFs, and prefer a virtual environment with pinned dependencies.

## Reference(s):

- [PDF Processing Guide](artifact/SKILL.md)
- [PDF Form Filling Guidance](artifact/forms.md)
- [PDF Processing Advanced Reference](artifact/reference.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with code snippets, shell commands, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce or modify local PDF, image, text, spreadsheet, or JSON files depending on the requested workflow.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
