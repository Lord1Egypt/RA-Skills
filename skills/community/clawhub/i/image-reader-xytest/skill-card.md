## Description: <br>
Recognizes text in local images, including Chinese-language content, using the OCR.space free API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xytest](https://clawhub.ai/user/xytest) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and end users use this skill to extract OCR text from local image files, especially Chinese-language content, by running the included Python script against a selected image. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Images submitted for OCR are uploaded to OCR.space, which may expose sensitive visual content to a third-party service. <br>
Mitigation: Use only images approved for third-party processing; avoid confidential IDs, financial records, medical documents, private screenshots, and regulated data unless that processing is acceptable. <br>
Risk: OCR output is saved locally as a text file and may retain sensitive content after processing. <br>
Mitigation: Review and delete generated OCR text files when they contain sensitive information. <br>


## Reference(s): <br>
- [OCR.space image parsing API endpoint](https://api.ocr.space/parse/image) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, files, guidance] <br>
**Output Format:** [Plain text OCR output with a generated UTF-8 .txt file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uploads the selected image to OCR.space and writes extracted text to a local *_ocr.txt file.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
