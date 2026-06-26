## Description: <br>
OCR Tool uses Tesseract to extract text from images, including screenshots, charts, documents, and Chinese or English financial announcement images. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liuzhengmcc-debug](https://clawhub.ai/user/liuzhengmcc-debug) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to run local OCR on selected image files, then extract plain text and basic financial entities such as company names, stock codes, metrics, and keywords. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: OCR can misread or omit characters, especially in financial charts, screenshots, or multilingual images. <br>
Mitigation: Verify extracted text and financial entities against the source image before using them for decisions. <br>
Risk: Images from Telegram caches, message folders, or sensitive documents may contain private information that becomes visible or saved as extracted text. <br>
Mitigation: Process only images intentionally selected for OCR and review where extracted text is stored or shared. <br>
Risk: The skill depends on local Tesseract installation and language data, so missing binaries or language packs can produce failures or poor OCR quality. <br>
Mitigation: Install Tesseract and the required language packs before use, then test on representative images. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/liuzhengmcc-debug/ocr-tool) <br>
- [Publisher profile](https://clawhub.ai/user/liuzhengmcc-debug) <br>
- [Tesseract OCR language data](https://github.com/tesseract-ocr/tessdata) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text OCR output, Markdown guidance, shell command examples, and Python dictionary results from the helper script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the local tesseract binary and appropriate language data; OCR results should be verified before relying on extracted financial data.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
