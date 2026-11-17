## Description:

PDF Toolkit helps agents process PDF and document workflows through the ComPDF Cloud REST API, including conversion, page editing, compression, OCR, comparison, and document extraction tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[compdf-youna](https://clawhub.ai/user/compdf-youna)

### License/Terms of Use:

Apache 2.0

## Use Case:

External users, developers, and document operations teams use this skill to route mixed PDF requests to ComPDF Cloud, choose the correct operation, build supported parameters, and return processing status, download links, or troubleshooting guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected documents are uploaded to ComPDF cloud servers for processing.

Mitigation: Proceed only after explicit user confirmation and avoid highly sensitive files unless the user's policy allows that service.

Risk: The ComPDF API key may be stored locally in plaintext when the user opts in.

Mitigation: Store the key only with user consent, keep it local, and delete config/public_key.txt when local credential storage is no longer acceptable.

Risk: A successful HTTP status does not guarantee successful document processing.

Mitigation: Check the response code and taskStatus fields, then use the documented error-code guidance before returning a result.

## Reference(s):

- [ComPDF API Reference](https://www.compdf.com/guides/api-reference/v2/overview?utm_source=clawhub&utm_medium=skillhub&utm_campaign=pdf_skill_pdf_toolkit&ref_platform_id=clawhub_skills)
- [Tool List](references/tool-list.md)
- [Parameter Details](references/parameters.md)
- [Error Code Reference](references/error-codes.md)
- [ClawHub Skill Page](https://clawhub.ai/compdf-youna/skills/pdf-tools-compdf)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Guidance]

**Output Format:** [Markdown status messages with file metadata, expiring download URLs, and troubleshooting guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference processed document files hosted by ComPDF Cloud; download links expire at 24:00 the next day.]

## Skill Version(s):

1.2.0 (source: evidence.release.version and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
