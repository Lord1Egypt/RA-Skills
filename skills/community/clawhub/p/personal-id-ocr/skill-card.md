## Description:

Recognizes front and back images of mainland China ID cards through the SCNet OCR API and extracts fields such as name, gender, ethnicity, birth date, address, ID number, issuing authority, and validity period.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scnet-sugon](https://clawhub.ai/user/scnet-sugon)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to send local ID-card images or PDFs to SCNet's OCR service and receive structured JSON fields for document-processing workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can upload sensitive ID-card or document images to SCNet's cloud OCR service.

Mitigation: Use it only with files intended for SCNet processing and confirm users are comfortable sending those documents to the external service before execution.

Risk: A configurable API base URL can redirect uploads if altered.

Mitigation: Keep SCNET_API_BASE pointed at the intended SCNet HTTPS endpoint and rotate the API key if the endpoint or config may have been changed.

Risk: The skill depends on a local API key stored in configuration or environment variables.

Mitigation: Store SCNET_API_KEY outside chat, protect config/.env with restrictive permissions, and rotate the key if it may have been exposed.

## Reference(s):

- [Sugon-Scnet OCR API Summary](references/api-docs.md)
- [ID Card Field Summary](assets/templates/fields-summary.md)
- [SCNet Website](https://www.scnet.cn)
- [ClawHub Skill Page](https://clawhub.ai/scnet-sugon/skills/personal-id-ocr)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Structured JSON on stdout with text error messages on failure]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SCNET_API_KEY; uploads the provided file to the configured SCNet OCR endpoint; removes per-item confidence before printing result data.]

## Skill Version(s):

1.0.3 (source: frontmatter, skill.yaml, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
