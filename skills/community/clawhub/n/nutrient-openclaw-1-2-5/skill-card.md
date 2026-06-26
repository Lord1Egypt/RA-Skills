## Description: <br>
OpenClaw-native PDF/document processing skill for Nutrient DWS for OpenClaw users who need PDF conversion, OCR, text/table extraction, PII redaction, watermarking, digital signatures, and API credit checks via built-in nutrient_* tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhouhuihui008](https://clawhub.ai/user/zhouhuihui008) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to process PDFs and other documents through Nutrient DWS from OpenClaw conversations. It supports conversion, OCR, extraction, redaction, watermarking, signing, and API credit checks when third-party document processing is acceptable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected documents or extracted document content are sent to Nutrient DWS for processing. <br>
Mitigation: Use the skill only when third-party processing is acceptable, start with non-sensitive sample files, and confirm Nutrient's security and privacy documentation against organizational requirements. <br>
Risk: Redactions, signatures, and other modified document outputs may be relied on before review. <br>
Mitigation: Manually verify redacted, signed, watermarked, converted, and extracted outputs before using them in production workflows. <br>
Risk: API credentials are required for the OpenClaw plugin configuration. <br>
Mitigation: Use a scoped API key where possible and avoid placing production credentials in shared examples or logs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhouhuihui008/nutrient-openclaw-1-2-5) <br>
- [Nutrient API](https://www.nutrient.io/api/) <br>
- [Nutrient Processor API security](https://www.nutrient.io/api/documentation/security) <br>
- [Nutrient Processor API](https://www.nutrient.io/api/processor-api/) <br>
- [Nutrient OpenClaw repository](https://github.com/PSPDFKit-labs/nutrient-openclaw) <br>
- [Nutrient OpenClaw npm package](https://www.npmjs.com/package/@nutrient-sdk/nutrient-openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and YAML configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May invoke Nutrient OpenClaw tools that send selected files or extracted document content to Nutrient DWS.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
