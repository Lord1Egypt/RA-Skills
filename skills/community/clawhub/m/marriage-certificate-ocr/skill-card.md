## Description:

Extracts marriage certificate holder, registration date, certificate number, names, birthdates, and identity numbers from local document images using the Sugon-Scnet OCR API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scnet-sugon](https://clawhub.ai/user/scnet-sugon)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to send a local marriage certificate image or PDF to Sugon-Scnet OCR and receive structured extracted fields for downstream review or workflow automation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uploads sensitive marriage-certificate documents to an external OCR provider.

Mitigation: Use it only for documents the user is allowed to send to Scnet, with consent and a valid data-handling reason.

Risk: The OCR API token and uploaded document data are sent to a configurable endpoint.

Mitigation: Keep SCNET_API_BASE set to the official HTTPS api.scnet.cn endpoint and avoid untrusted alternate endpoints.

Risk: The provider privacy and retention terms are not established by the release evidence.

Mitigation: Verify Scnet privacy and retention terms before processing real identity documents.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/scnet-sugon/skills/marriage-certificate-ocr)
- [Scnet website](https://www.scnet.cn)
- [Sugon-Scnet OCR API docs](references/api-docs.md)
- [Marriage certificate field summary](assets/templates/fields-summary.md)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration]

**Output Format:** [JSON printed to standard output, with text error messages on failure]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SCNET_API_KEY and accepts an optional SCNET_API_BASE endpoint.]

## Skill Version(s):

1.0.0 (source: frontmatter, skill.yaml, changelog, and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
