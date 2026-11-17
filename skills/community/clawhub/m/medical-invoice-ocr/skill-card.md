## Description:

Recognizes medical invoices with the Sugon-Scnet OCR API and returns structured JSON fields.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scnet-sugon](https://clawhub.ai/user/scnet-sugon)

### License/Terms of Use:

MIT

## Use Case:

Employees, external users, and developers can use this skill to extract structured fields from medical invoice images, PDFs, or supported archives through the Scnet OCR service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Medical invoices may contain sensitive personal or billing information and are uploaded to the Scnet OCR service.

Mitigation: Use the skill only after confirming the selected document may be sent to Scnet, especially for real medical invoices.

Risk: The API base URL is configurable, which could route sensitive documents away from the intended service if changed.

Mitigation: Keep SCNET_API_BASE fixed to the official HTTPS endpoint unless a trusted operator has reviewed and approved the alternate endpoint.

Risk: The skill requires an SCNET_API_KEY credential.

Mitigation: Store the key in an environment variable or protected config file, avoid pasting it into chats, and rotate it if exposure is suspected.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/scnet-sugon/skills/medical-invoice-ocr)
- [Publisher profile](https://clawhub.ai/user/scnet-sugon)
- [Scnet website](https://www.scnet.cn)
- [Sugon-Scnet OCR API docs](references/api-docs.md)
- [Medical invoice field summary](assets/templates/fields-summary.md)

## Skill Output:

**Output Type(s):** [Text, Configuration]

**Output Format:** [JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an OCR type and a local file path; returns OCR results for submitted medical invoice files.]

## Skill Version(s):

1.1.3 (source: frontmatter, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
