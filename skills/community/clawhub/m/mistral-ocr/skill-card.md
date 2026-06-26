## Description: <br>
Extract text, tables, and images from PDFs or images using Mistral OCR API and output in Markdown, JSON, or HTML formats. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[YZDame](https://clawhub.ai/user/YZDame) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and document-processing users use this skill to run Mistral OCR on PDFs or images and save extracted text, tables, and images as Markdown, JSON, or HTML. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Input files are uploaded to Mistral cloud processing, which may be inappropriate for sensitive or confidential documents. <br>
Mitigation: Use only when Mistral cloud processing is acceptable; use offline OCR for sensitive documents and review Mistral privacy terms before processing. <br>
Risk: The open-ended Mistral SDK dependency allows a known compromised SDK release in the permitted range. <br>
Mitigation: Install in an isolated environment with a dependency lock or constraint that excludes mistralai==2.4.6 and verifies the resolved SDK version. <br>
Risk: A long-lived Mistral API key can be exposed if it is stored in shell profiles or logs. <br>
Mitigation: Use a secrets manager or a temporary environment variable and avoid committing or logging MISTRAL_API_KEY. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/YZDame/mistral-ocr) <br>
- [Mistral API console](https://console.mistral.ai/home) <br>
- [Mistral privacy policy](https://mistral.ai/privacy-policy) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Files] <br>
**Output Format:** [Markdown, JSON, or HTML files with extracted image files when available] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MISTRAL_API_KEY and uploads input documents to Mistral cloud OCR.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
