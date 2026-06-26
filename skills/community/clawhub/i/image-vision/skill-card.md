## Description: <br>
Analyze images with multimodal vision models to describe visual content, extract text, answer questions, compare images, and extract structured data from JPG, PNG, GIF, and WebP files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cntuang](https://clawhub.ai/user/cntuang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and agents use this skill to inspect user-supplied images, perform OCR, answer visual questions, compare images, and extract structured details from receipts, forms, screenshots, charts, or documents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User-supplied images may contain secrets, IDs, payment details, account numbers, private business information, authentication material, or regulated data. <br>
Mitigation: Redact sensitive details before analysis and avoid submitting regulated or confidential content unless the use case requires it. <br>
Risk: OCR, visual descriptions, comparisons, or extracted fields may be incomplete or incorrect. <br>
Mitigation: Review outputs against the source image before relying on them for decisions or downstream automation. <br>


## Reference(s): <br>
- [Image Vision on ClawHub](https://clawhub.ai/cntuang/image-vision) <br>
- [cntuang publisher profile](https://clawhub.ai/user/cntuang) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown or plain text responses from the active multimodal model] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include visual descriptions, OCR text, image comparisons, content-moderation assessments, or structured key-value extractions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
