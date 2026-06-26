## Description: <br>
Batch OCR for scanned PDFs that creates searchable PDFs and can support downstream text or Markdown extraction for teacher-agent document workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[openclawzhangchong](https://clawhub.ai/user/openclawzhangchong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Educators, developers, and automation agents use this skill to OCR scanned PDF collections before ingestion, vectorization, search, or review. It is especially suited to teacher-agent workflows that need searchable text from scanned teaching materials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Batch or scheduled OCR runs can process unintended PDFs or create repeated output files when pointed at broad directories. <br>
Mitigation: Run the script on copies of important PDFs first, restrict batch and scheduled runs to intended OCR directories, and monitor output folders. <br>
Risk: OCR execution depends on local Tesseract and ocrmypdf installations from the host environment. <br>
Mitigation: Install OCR dependencies from trusted sources and verify the tools before processing documents. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/openclawzhangchong/pdf-ocr-zc) <br>
- [Install Tesseract and ocrmypdf](references/install_ocr.md) <br>
- [OCR parameters and tips](references/ocr_tips.md) <br>
- [UB Mannheim Tesseract Windows builds](https://github.com/UB-Mannheim/tesseract/wiki) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and a Python helper script.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Local PDF processing; produces searchable PDF files and may be followed by text or Markdown extraction.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
