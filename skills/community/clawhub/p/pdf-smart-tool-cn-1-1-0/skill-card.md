## Description: <br>
PDF Smart Tool helps agents handle PDF conversion, OCR, merge and split workflows, digital signatures, batch processing, watermarking, encryption, and decryption. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sunyue1977](https://clawhub.ai/user/sunyue1977) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and document-workflow teams use this skill to ask an agent for PDF conversion, OCR extraction, document assembly, signing, watermarking, encryption, decryption, and batch-processing help. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles sensitive PDFs and may expose document contents during OCR, conversion, or extraction workflows. <br>
Mitigation: Use it only with documents the user is authorized to process and avoid sharing unnecessary sensitive content. <br>
Risk: Batch operations, decryption, signing, watermark removal, and format conversion can modify important files or remove protections. <br>
Mitigation: Confirm file lists and requested actions before processing, and keep backups before any destructive or irreversible operation. <br>
Risk: Password or certificate prompts can involve sensitive credentials. <br>
Mitigation: Avoid unnecessary password or certificate entry and prefer user-controlled credential handling. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sunyue1977/pdf-smart-tool-cn-1-1-0) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown and plain-language instructions, with shell commands when PDF tools are needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference local PDF utilities including pdftotext, tesseract, and ghostscript.] <br>

## Skill Version(s): <br>
1.1.0 (source: SKILL.md frontmatter and artifact/_meta.json; server release metadata: 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
