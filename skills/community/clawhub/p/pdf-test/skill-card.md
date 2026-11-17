## Description:

Use this skill whenever the user wants to do anything with PDF files, including reading or extracting text and tables, merging, splitting, rotating, watermarking, creating, filling, encrypting or decrypting PDFs, extracting images, and OCR on scanned PDFs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gitasura](https://clawhub.ai/user/gitasura)

### License/Terms of Use:

Proprietary

## Use Case:

Developers and agents use this skill to operate on local PDF files, including extracting content, modifying documents, filling forms, converting pages to images, and producing validation artifacts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: PDF operations can overwrite originals or create sensitive decrypted output files.

Mitigation: Use explicit input and output paths, avoid writing over source documents, and handle decrypted PDFs as sensitive files.

Risk: Optional OCR and PDF conversion dependencies can add supply-chain and environment risk.

Mitigation: Install optional dependencies only when needed, use an isolated environment, and pin dependency versions where possible.

Risk: Manually estimated PDF form coordinates can place annotations incorrectly.

Mitigation: Validate bounding boxes before filling forms and convert completed PDFs to images for placement review.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gitasura/skills/pdf-test)
- [PDF form guidance](artifact/forms.md)
- [PDF processing advanced reference](artifact/reference.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python, JavaScript, shell command, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce or modify local PDF, PNG, JSON, text, spreadsheet, and image files when the referenced scripts or examples are run.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
