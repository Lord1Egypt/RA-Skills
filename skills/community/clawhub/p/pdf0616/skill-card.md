## Description:

Use this skill whenever the user wants to do anything with PDF files, including reading or extracting text and tables, merging, splitting, rotating, watermarking, creating, filling, encrypting or decrypting, extracting images, and OCR on scanned PDFs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aredkuku](https://clawhub.ai/user/aredkuku)

### License/Terms of Use:

Proprietary

## Use Case:

Developers, engineers, and agent operators use this skill to guide local PDF processing workflows such as extraction, conversion, form filling, document creation, encryption, and OCR.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: PDF processing commands and scripts may read sensitive local PDFs and create derived PDFs, images, JSON, or text files.

Mitigation: Run the skill only on documents the user is authorized to process, keep outputs in an expected workspace, and review generated files before sharing them.

Risk: Password removal, decryption, repair, or overwrite examples can affect protected or original documents.

Mitigation: Use these commands only for documents the user owns or is authorized to unlock, and make backups before any repair or overwrite operation.

## Reference(s):

- [PDF Processing Guide](artifact/SKILL.md)
- [PDF Form Filling Guide](artifact/forms.md)
- [PDF Processing Advanced Reference](artifact/reference.md)
- [ClawHub Skill Page](https://clawhub.ai/aredkuku/skills/pdf0616)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python, JavaScript, JSON, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local PDF, image, JSON, and text files when its commands or scripts are run by an agent.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
