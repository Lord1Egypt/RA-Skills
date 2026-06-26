## Description: <br>
Extracts text from local image files with Chinese and English OCR using Tesseract. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[igetmm](https://clawhub.ai/user/igetmm) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and automation agents use this skill to extract text from local image files, including mixed Chinese and English content, for downstream reading or processing workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Image files may contain sensitive text that becomes visible in OCR output. <br>
Mitigation: Process only images intended for OCR and store generated text or JSON output in trusted locations. <br>
Risk: The skill depends on Tesseract, pytesseract, and Pillow being installed safely and correctly. <br>
Mitigation: Install dependencies from trusted system and Python package repositories before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/igetmm/image-ocr-reader) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Files, Shell commands, Guidance] <br>
**Output Format:** [Plain text or JSON; optional UTF-8 text file output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Detailed mode can include OCR confidence and bounding-box data.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence, artifact metadata, and __init__.py) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
