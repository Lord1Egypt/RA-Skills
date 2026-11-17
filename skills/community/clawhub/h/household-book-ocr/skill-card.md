## Description:

Household Book Ocr extracts text and household-register fields from local images, PDFs, or archives by uploading the file to the Scnet cloud OCR API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scnet-sugon](https://clawhub.ai/user/scnet-sugon)

### License/Terms of Use:

MIT

## Use Case:

External users and agents use this skill to OCR Chinese household-register documents and return structured identity fields for downstream review or processing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Household-register images or PDFs may contain sensitive identity data and are uploaded to Scnet's cloud OCR service.

Mitigation: Confirm with the user before each document upload and use the skill only when the user accepts that external processing.

Risk: The API token and document can be sent to a configurable external API base URL.

Mitigation: Keep SCNET_API_BASE fixed to the documented Scnet HTTPS endpoint and do not paste SCNET_API_KEY into chat.

Risk: Runtime dependencies and network behavior affect the trust boundary for OCR processing.

Mitigation: Use a dedicated environment with pinned dependencies when possible and review the command before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/scnet-sugon/skills/household-book-ocr)
- [Sugon-Scnet OCR API documentation](references/api-docs.md)
- [Household register field summary](assets/templates/fields-summary.md)
- [Scnet website](https://www.scnet.cn)

## Skill Output:

**Output Type(s):** [text]

**Output Format:** [JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Structured OCR data from the API response; the script removes per-item confidence fields before printing.]

## Skill Version(s):

1.0.8 (source: frontmatter, skill.yaml, ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
