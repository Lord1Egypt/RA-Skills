## Description: <br>
This skill helps agents read, extract, transform, create, fill, secure, and OCR PDF files using Python libraries and command-line tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gitasura](https://clawhub.ai/user/gitasura) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to perform common PDF workflows such as text and table extraction, page manipulation, PDF creation, form filling, OCR, and password handling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads and writes local PDF-derived files that may contain sensitive content. <br>
Mitigation: Use copies for important documents, process sensitive PDFs only when necessary, and delete generated images, JSON, or derived files when they contain private content. <br>
Risk: The skill includes workflows for decrypting or removing PDF passwords. <br>
Mitigation: Only decrypt or remove passwords when authorized, and avoid putting real passwords in shared logs or shell history. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gitasura/pdf-test) <br>
- [PDF Processing Guide](artifact/SKILL.md) <br>
- [PDF Form Filling Guide](artifact/forms.md) <br>
- [PDF Processing Advanced Reference](artifact/reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline code blocks, shell commands, and generated local PDF, image, text, JSON, or spreadsheet files when the agent runs the referenced tools.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include local derivative files from source PDFs, including filled PDFs, page images, extracted text, form-field JSON, and validation images.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
