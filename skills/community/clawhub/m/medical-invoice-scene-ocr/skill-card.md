## Description:

Recognizes medical reimbursement documents, including inpatient medical invoices and medical expense settlement forms, after the user provides a local file path and confirms upload to the Scnet OCR API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scnet-sugon](https://clawhub.ai/user/scnet-sugon)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use this skill to submit local medical invoice or settlement-form images to Scnet OCR and receive structured recognition results for reimbursement workflows. It should be used only after explicit user confirmation because source documents can contain sensitive health and identity information.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Medical invoices and settlement forms can contain sensitive health and identity information and are uploaded to an external OCR API.

Mitigation: Require explicit consent and a verified local file path before each upload, and use the skill only when the file owner has authorized third-party processing.

Risk: The API base URL is configurable, which could send sensitive documents to an unintended endpoint.

Mitigation: Keep SCNET_API_BASE set to the official HTTPS Scnet endpoint unless another endpoint has been independently vetted.

Risk: The skill depends on an API key and an unpinned requests dependency.

Mitigation: Store SCNET_API_KEY outside chat, restrict config file permissions, and prefer a pinned dependency or isolated environment before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/scnet-sugon/skills/medical-invoice-scene-ocr)
- [ClawHub publisher profile](https://clawhub.ai/user/scnet-sugon)
- [Sugon-Scnet OCR API documentation summary](references/api-docs.md)
- [Field summary](assets/templates/fields-summary.md)
- [Scnet website](https://www.scnet.cn)
- [Scnet OCR API endpoint](https://api.scnet.cn/api/llm/v1)

## Skill Output:

**Output Type(s):** [JSON, Text, Shell commands, Configuration]

**Output Format:** [Structured JSON recognition data with text error messages on failure]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns OCR result data for one submitted local file; result fields vary by ocrType.]

## Skill Version(s):

0.1.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
