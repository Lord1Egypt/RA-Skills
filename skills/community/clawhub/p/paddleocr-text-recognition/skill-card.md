## Description: <br>
Extracts text from images, photos, scans, screenshots, and scanned PDFs using PaddleOCR, returning machine-readable line text and optional bounding boxes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bobholamovic](https://clawhub.ai/user/bobholamovic) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to extract plain text and line-level OCR data from images, screenshots, scans, photos, and scanned PDFs. It is best suited for text recognition workflows rather than complex document parsing with tables, formulas, or charts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad OCR trigger wording could make the skill activate more often than users expect. <br>
Mitigation: Prefer explicit OCR requests, such as asking to extract text from a specific image, screenshot, scan, or PDF. <br>
Risk: Input screenshots, photos, or PDFs may contain passwords, personal records, financial data, private messages, or other sensitive information. <br>
Mitigation: Review inputs before OCR and avoid sending sensitive material unless extraction is intentional and appropriate. <br>
Risk: The PaddleOCR API requires a valid access token and may fail because of missing credentials, invalid credentials, or quota limits. <br>
Mitigation: Check that PADDLEOCR_ACCESS_TOKEN is configured and report authentication or quota errors clearly to the user. <br>


## Reference(s): <br>
- [PaddleOCR Official API CLI Documentation](https://www.paddleocr.ai/latest/en/version3.x/inference_deployment/serving/paddleocr_official_api/cli.html) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with bash command examples and OCR text or JSON results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include line-level recognized text, confidence scores, optional bounding boxes, page-level results, and authentication or quota error guidance.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
