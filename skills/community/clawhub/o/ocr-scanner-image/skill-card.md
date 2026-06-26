## Description: <br>
Perform OCR on image files (jpg, png, bmp, gif, tiff) using the system's `tesseract` binary and return extracted plain text. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kaarl92](https://clawhub.ai/user/kaarl92) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to extract plain text from local image files through Tesseract OCR. The package also contains an optional OCR.space API helper, which should be treated separately from the local workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The package presents local Tesseract OCR as the main behavior while also shipping a cloud OCR helper that can send selected images or URLs to OCR.space. <br>
Mitigation: Use scripts/ocr.sh for local processing, and do not run scripts/example.py unless cloud OCR data transfer is acceptable for the input. <br>
Risk: Sensitive documents could be exposed if the OCR.space helper is used without clear opt-in consent. <br>
Mitigation: Avoid the cloud helper for sensitive documents unless the package is updated to clearly disclose the data flow and require explicit opt-in. <br>


## Reference(s): <br>
- [Reference Documentation for Ocr](references/api_reference.md) <br>
- [OCR.space API endpoint](https://api.ocr.space/parse/image) <br>
- [OCR.space API documentation](https://ocr.space/ocrapi) <br>
- [ClawHub skill page](https://clawhub.ai/kaarl92/ocr-scanner-image) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text from OCR commands, with Markdown usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Local OCR uses the system Tesseract binary and writes recognized text to STDOUT; the optional OCR.space helper returns extracted text or error messages.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; SKILL.md frontmatter says 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
