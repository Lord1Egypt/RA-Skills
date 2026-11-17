## Description:

OpenClaw-native document processing skill for Nutrient DWS that supports PDF conversion, OCR, text and table extraction, redaction, watermarking, digital signatures, and API credit checks through built-in nutrient_* tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhouhuihui008](https://clawhub.ai/user/zhouhuihui008)

### License/Terms of Use:

MIT-0

## Use Case:

External OpenClaw users and developers use this skill to process documents in OpenClaw conversations with Nutrient DWS tools for conversion, extraction, OCR, redaction, signing, watermarking, and credit checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected documents or extracted content are sent to Nutrient DWS for processing.

Mitigation: Use the skill only when third-party document processing is acceptable, and confirm Nutrient retention, privacy, and security terms before using sensitive or regulated documents.

Risk: The skill requires a Nutrient API key in OpenClaw plugin configuration.

Mitigation: Use a dedicated revocable API key and rotate it if exposure is suspected.

Risk: The install flow does not pin the npm package version in the available evidence.

Mitigation: Prefer a pinned, reviewed package version when OpenClaw supports version pinning.

## Reference(s):

- [Nutrient API](https://www.nutrient.io/api/)
- [Nutrient Processor API Security Documentation](https://www.nutrient.io/api/documentation/security)
- [Nutrient Processor API](https://www.nutrient.io/api/processor-api/)
- [Nutrient OpenClaw Repository](https://github.com/PSPDFKit-labs/nutrient-openclaw)
- [Nutrient OpenClaw npm Package](https://www.npmjs.com/package/@nutrient-sdk/nutrient-openclaw)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands, YAML configuration snippets, and document-processing outputs from Nutrient tools.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Nutrient API key configured in OpenClaw.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
