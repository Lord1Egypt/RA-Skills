## Description: <br>
OpenClaw-native PDF and document processing skill that helps users convert, OCR, extract, redact, watermark, sign, and check credits through Nutrient DWS. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jdrhyne](https://clawhub.ai/user/jdrhyne) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to process PDFs and other documents in OpenClaw conversations, including conversion, OCR, text and table extraction, redaction, watermarking, signing, and API credit checks. It is appropriate when sending selected documents or extracted document content to Nutrient DWS is acceptable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected documents or extracted document content are sent to Nutrient DWS for processing. <br>
Mitigation: Use the skill only when third-party document processing is acceptable, start with non-sensitive sample files, and confirm Nutrient's security and privacy details against organizational requirements. <br>
Risk: Redaction, signing, and watermarking outputs may not meet requirements without review. <br>
Mitigation: Review generated outputs before relying on them, especially for sensitive documents, legal signatures, or production redaction workflows. <br>
Risk: A broad or shared API key could increase exposure if misused. <br>
Mitigation: Use a dedicated Nutrient API key where possible and rotate or scope credentials according to organizational policy. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jdrhyne/nutrient-openclaw) <br>
- [Nutrient API](https://www.nutrient.io/api/) <br>
- [Nutrient Processor API security](https://www.nutrient.io/api/documentation/security) <br>
- [Nutrient Processor API](https://www.nutrient.io/api/processor-api/) <br>
- [Nutrient OpenClaw repository](https://github.com/PSPDFKit-labs/nutrient-openclaw) <br>
- [Nutrient OpenClaw npm package](https://www.npmjs.com/package/@nutrient-sdk/nutrient-openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [text, files, configuration, guidance] <br>
**Output Format:** [OpenClaw tool results, processed document files, extracted text or tables, and Markdown guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a configured Nutrient API key and sends selected documents or extracted content to Nutrient DWS.] <br>

## Skill Version(s): <br>
1.2.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
