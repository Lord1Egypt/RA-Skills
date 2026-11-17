## Description:

A Chinese-language PDF assistant for conversion, OCR, merging and splitting, digital signatures, batch processing, watermarking, and encryption workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sunyue1977](https://clawhub.ai/user/sunyue1977)

### License/Terms of Use:

MIT-0

## Use Case:

External users and business document teams use this skill to guide PDF conversion, OCR, signing, watermarking, encryption, decryption, and batch document handling workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: PDF workflows may expose confidential documents, passwords, signatures, certificates, or regulated content to agent processing.

Mitigation: Use only with documents you are comfortable processing in the agent environment, and avoid sensitive files unless the deployment is approved for that content.

Risk: Decryption, watermark removal, batch renaming, signing, and similar document edits may be hard to reverse.

Mitigation: Keep backups and review proposed operations before allowing the agent to modify or generate final PDF outputs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sunyue1977/skills/pdf-smart-tool-cn-1-1-0)
- [ClawHub publisher profile](https://clawhub.ai/user/sunyue1977)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with file, command, and workflow examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose PDF-processing steps that operate on local documents and depend on pdftotext, tesseract, and ghostscript.]

## Skill Version(s):

1.1.0 (source: artifact/SKILL.md frontmatter and artifact/_meta.json; ClawHub release metadata version: 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
