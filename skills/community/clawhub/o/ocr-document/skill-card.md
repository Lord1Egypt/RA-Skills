## Description: <br>
OCR document extraction - extract text from scanned documents, photos, and images using OCR. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tanis90](https://clawhub.ai/user/tanis90) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to extract text from scanned PDFs, photographed pages, handwritten notes, and document images using the MinerU Open API CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Documents are sent to MinerU's cloud service for OCR processing. <br>
Mitigation: Use the skill only for documents appropriate for that service, and avoid highly sensitive documents unless MinerU's privacy terms meet the user's needs. <br>
Risk: Optional higher-precision OCR mode requires authenticated MinerU CLI usage. <br>
Mitigation: Use authenticated mode only intentionally, after confirming the account and credential posture are appropriate. <br>


## Reference(s): <br>
- [Ocr Document on ClawHub](https://clawhub.ai/tanis90/ocr-document) <br>
- [MinerU](https://mineru.net) <br>
- [MinerU CLI Downloads](https://mineru.net/ecosystem?tab=cli) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with OCR text results and inline bash commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports local files and URLs; input documents are limited to 10MB or 20 pages.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
