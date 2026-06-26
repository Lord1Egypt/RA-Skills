## Description: <br>
Helps agents read, extract, transform, create, fill, encrypt or decrypt, OCR, and otherwise process PDF files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qinghong268](https://clawhub.ai/user/qinghong268) <br>

### License/Terms of Use: <br>
Proprietary <br>


## Use Case: <br>
Developers, document-workflow builders, and agent users use this skill to perform local PDF operations such as text and table extraction, PDF creation, page manipulation, OCR, image extraction, and form filling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: PDF repair, form filling, decryption, and similar workflows can create overwritten, transformed, or newly exposed local files. <br>
Mitigation: Keep backups before repair or overwrite-style operations, run commands only on PDFs intended for processing, and protect extracted text, images, JSON, and decrypted PDFs. <br>
Risk: The skill relies on local PDF libraries and command-line tools for some workflows. <br>
Mitigation: Install required PDF tools and Python packages from trusted sources and review proposed commands before execution. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/qinghong268/pdf-qinghong) <br>
- [PDF Processing Guide](artifact/SKILL.md) <br>
- [PDF Forms Guide](artifact/forms.md) <br>
- [PDF Processing Advanced Reference](artifact/reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, files, guidance] <br>
**Output Format:** [Markdown guidance with code blocks, shell commands, JSON examples, and generated local PDF-related files when scripts are run.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May generate or modify local PDFs, images, JSON, text, or decrypted PDF outputs depending on the selected workflow.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
