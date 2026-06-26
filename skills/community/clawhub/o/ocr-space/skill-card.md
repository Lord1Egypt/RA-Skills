## Description: <br>
Uses the OCR.space free API to recognize text in images, with multilingual support and command-line or Python usage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[juguangyuan520-dotcom](https://clawhub.ai/user/juguangyuan520-dotcom) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to extract text from user-selected image files through OCR.space, especially for workflows that can use the free API limits. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected image files are sent to OCR.space for processing. <br>
Mitigation: Avoid using the skill with IDs, invoices, private screenshots, medical records, or other sensitive images unless that matches the user's privacy expectations. <br>
Risk: The free OCR.space API has usage and file-size limits that can affect reliability for larger or higher-volume workloads. <br>
Mitigation: Use the skill for workflows that fit the documented free limits, or switch to a paid OCR.space plan for production workloads that need higher limits. <br>


## Reference(s): <br>
- [OCR.space OCR API documentation](https://ocr.space/ocrapi) <br>
- [ClawHub skill page](https://clawhub.ai/juguangyuan520-dotcom/ocr-space) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Plain text OCR results with Markdown usage examples and Python or shell invocation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Sends selected image content to OCR.space; free API usage is documented as 500 requests per day and 5 MB per file.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
