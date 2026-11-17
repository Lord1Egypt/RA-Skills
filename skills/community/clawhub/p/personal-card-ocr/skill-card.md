## Description:

Extracts structured OCR data from user-provided images or PDFs of personal identity, banking, travel, education, marriage, real estate, and vehicle documents by uploading the selected file to Scnet's OCR API after user consent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scnet-sugon](https://clawhub.ai/user/scnet-sugon)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to recognize text and structured fields from specific user-provided document images or PDFs through Scnet OCR. It is intended for cases where the user explicitly requests OCR and agrees that the selected file may be uploaded to a third-party service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected files may contain sensitive personal information and are uploaded to Scnet for OCR processing.

Mitigation: Use only with explicit user consent, upload only the minimum necessary document, and do not process other people's documents without permission.

Risk: The executable can use an arbitrary configured API endpoint through SCNET_API_BASE.

Mitigation: Before use, verify local configuration points to https://api.scnet.cn/api/llm/v1 and keep endpoint configuration under local administrative control.

Risk: SCNET_API_KEY is required and could be exposed if handled insecurely.

Mitigation: Treat the API key as a secret and store it only in a local environment variable or restricted config/.env file.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/scnet-sugon/skills/personal-card-ocr)
- [Scnet OCR API documentation](references/api-docs.md)
- [OCR field summary](assets/templates/fields-summary.md)
- [Scnet OCR API endpoint](https://api.scnet.cn/api/llm/v1)

## Skill Output:

**Output Type(s):** [JSON, text, shell commands, configuration, guidance]

**Output Format:** [JSON OCR results with text error messages and setup guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SCNET_API_KEY and a user-specified local file path; OCR result fields vary by ocrType.]

## Skill Version(s):

1.0.6 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
