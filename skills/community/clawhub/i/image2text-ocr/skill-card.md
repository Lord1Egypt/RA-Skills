## Description:

Extracts text from image files by calling the Sugon-Scnet OCR API and returning structured recognition results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scnet-sugon](https://clawhub.ai/user/scnet-sugon)

### License/Terms of Use:

MIT

## Use Case:

Developers and external users use this skill to extract text and layout data from local images, PDFs, or compressed document inputs through the Sugon-Scnet OCR service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uploads local OCR files to the SCNet remote service.

Mitigation: Use it only for documents appropriate for that provider, and verify the provider's privacy terms before processing sensitive files.

Risk: The API key is read from config/.env and sent to a configurable remote endpoint.

Mitigation: Keep config/.env private, avoid pasting API keys into chat, and change SCNET_API_BASE only to endpoints you fully trust.

## Reference(s):

- [Sugon-Scnet OCR API documentation](artifact/references/api-docs.md)
- [OCR field summary](artifact/assets/templates/fields-summary.md)
- [SCNet service](https://www.scnet.cn)
- [ClawHub skill page](https://clawhub.ai/scnet-sugon/skills/image2text-ocr)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration guidance]

**Output Format:** [JSON emitted to stdout, with human-readable error text on failure]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SCNET_API_KEY; uploads a local file to the configured SCNet OCR endpoint and returns the response data array.]

## Skill Version(s):

1.0.4 (source: SKILL.md frontmatter, skill.yaml, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
