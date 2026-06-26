## Description: <br>
Extract text from image-based or scanned PDFs using Tesseract OCR. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bilicen700](https://clawhub.ai/user/bilicen700) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and document-processing users use this skill to extract OCR text from scanned or image-based PDFs locally, without sending documents to third-party APIs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive PDF contents may be rendered into temporary page images during OCR. <br>
Mitigation: Run the skill in a trusted environment, use secure per-run temporary files, store temporary images only under /tmp, and delete them immediately after extraction. <br>
Risk: OCR behavior depends on local Tesseract, language packs, and Python packages being present and trustworthy. <br>
Mitigation: Install Tesseract, language data packs, pypdfium2, pytesseract, and Pillow from trusted package sources before use; do not download or install dependencies dynamically at runtime. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bilicen700/pdf-ocr-extraction) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with Python and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires local Tesseract, language data packs, Python 3, pypdfium2, pytesseract, and Pillow; temporary page images should be cleaned up after OCR.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
