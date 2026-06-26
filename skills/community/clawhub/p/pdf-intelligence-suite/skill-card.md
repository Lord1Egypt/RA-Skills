## Description: <br>
PDF Intelligence Suite extracts text and tables, performs OCR, converts PDFs to Word, Excel, images, text, and HTML, and supports page and security operations on local PDF files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kaiyuelv](https://clawhub.ai/user/kaiyuelv) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and document-automation teams use this skill to add local PDF extraction, OCR, conversion, table export, page manipulation, metadata, watermarking, encryption, and decryption workflows to an agent or Python project. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: PDF page deletion, decryption, watermarking, conversion, and other write operations can alter sensitive documents or produce unexpected output. <br>
Mitigation: Run the skill on copies of source PDFs and review generated files before replacing originals or sharing results. <br>
Risk: Very large or untrusted PDFs can consume excessive local resources during parsing, image conversion, OCR, or table extraction. <br>
Mitigation: Apply page and file-size limits before processing and avoid untrusted documents unless the execution environment is constrained. <br>
Risk: OCR and conversion quality depends on Tesseract, language packs, document layout, and installed Python dependencies. <br>
Mitigation: Install the documented dependencies and validate extracted text, tables, and converted files against representative documents before relying on the results. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/kaiyuelv/pdf-intelligence-suite) <br>
- [Project homepage](https://github.com/kaiyuelv/pdf-intelligence-suite) <br>
- [Tesseract OCR installation wiki](https://github.com/UB-Mannheim/tesseract/wiki) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Code, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown guidance with Python code and shell commands; runtime functions produce extracted text, tables, images, Office files, text files, HTML, and modified PDFs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Local file processing; OCR requires Tesseract and appropriate language packs.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, setup.py, __init__.py, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
