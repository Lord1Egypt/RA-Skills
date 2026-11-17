## Description:

Markdown convert processes, converts, edits, and extracts data from PDF files using the ComPDF Cloud API, including format conversion, page manipulation, watermarking, compression, OCR, and document extraction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[compdf-youna](https://clawhub.ai/user/compdf-youna)

### License/Terms of Use:

Apache 2.0

## Use Case:

Developers and external users use this skill to route PDF conversion, page editing, compression, watermarking, OCR, and document extraction tasks through ComPDF Cloud after confirming upload consent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected documents are uploaded to ComPDF's servers for processing.

Mitigation: Require explicit user confirmation before upload and avoid highly sensitive PDFs unless the user's organization accepts that handling.

Risk: The API public key can be stored locally in a plaintext config file when the user opts in.

Mitigation: Prefer session-only API-key use for sensitive environments; if saved, the user can delete config/public_key.txt to remove local storage.

## Reference(s):

- [ComPDF API Reference](https://www.compdf.com/guides/api-reference/v2/overview?utm_source=clawhub&utm_medium=skillhub&utm_campaign=pdf_skill_md_convert&ref_platform_id=clawhub_skills)
- [ComPDF API Complete Tool Type Reference](references/tool-list.md)
- [ComPDF API Tool Parameter Details](references/parameters.md)
- [ComPDF API Error Code Reference](references/error-codes.md)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown status messages with API parameters, troubleshooting guidance, and download links for processed files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uploads selected files to ComPDF Cloud only after explicit user confirmation; download links expire at 24:00 the next day.]

## Skill Version(s):

1.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
