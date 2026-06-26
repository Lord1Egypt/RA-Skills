## Description: <br>
Use this skill whenever the user wants to do anything with PDF files, including reading or extracting text and tables, merging, splitting, rotating, watermarking, creating, filling forms, encrypting or decrypting, extracting images, and OCR on scanned PDFs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pupuking723](https://clawhub.ai/user/pupuking723) <br>

### License/Terms of Use: <br>
Proprietary <br>


## Use Case: <br>
Developers, analysts, and other agent users use this skill to work with local PDF files, including extraction, transformation, generation, form filling, OCR, and security-related PDF operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: PDF workflows may read sensitive local documents or produce derived files containing sensitive content. <br>
Mitigation: Confirm which PDFs are being read, use new output filenames, and store generated files only in approved locations. <br>
Risk: Repair, form filling, annotation, merge, split, encryption, and decryption workflows can alter document contents or access controls. <br>
Mitigation: Keep backups before repair or transformation steps, review filled or modified PDFs before use, and only decrypt or remove passwords from documents the user is authorized to access. <br>
Risk: OCR and visual form-filling workflows can misread scanned content or place annotations inaccurately. <br>
Mitigation: Use the provided structure extraction, bounding-box validation, validation images, and final visual review steps before relying on the output. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/pupuking723/pdf-anthropic) <br>
- [PDF Processing Guide](artifact/SKILL.md) <br>
- [PDF form filling guide](artifact/forms.md) <br>
- [PDF Processing Advanced Reference](artifact/reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files, Guidance] <br>
**Output Format:** [Markdown with Python, JavaScript, shell command examples, and JSON file templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce or modify local PDF, PNG, JSON, text, spreadsheet, and image-derived files depending on the selected workflow.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
