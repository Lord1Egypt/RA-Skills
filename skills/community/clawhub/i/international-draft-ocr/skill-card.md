## Description:

Reads local international draft images, PDFs, or archives only after explicit upload consent, sends them to Scnet OCR, and returns structured fields such as payee, drawee bank, amount, dates, and draft number.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scnet-sugon](https://clawhub.ai/user/scnet-sugon)

### License/Terms of Use:

MIT

## Use Case:

External users and agents use this skill to extract structured information from international draft documents after confirming that the selected file may be uploaded to Scnet for OCR processing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected bill files may contain sensitive financial information and leave the local environment for OCR processing.

Mitigation: Use the skill only when the user is authorized to send the document to Scnet and has explicitly confirmed upload consent.

Risk: The configurable SCNET_API_BASE can redirect uploads and credentials away from the intended Scnet destination.

Mitigation: Verify before every use that SCNET_API_BASE is exactly the intended HTTPS Scnet API base.

Risk: SCNET_API_KEY may be exposed through chat, logs, or an insecure config file.

Mitigation: Keep config/.env private, avoid pasting the API key into chats, and restrict local file permissions.

Risk: Installing dependencies directly into a shared environment can increase supply-chain and environment-contamination risk.

Mitigation: Install pinned dependencies in an isolated environment before running the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/scnet-sugon/skills/international-draft-ocr)
- [Sugon-Scnet OCR API documentation summary](references/api-docs.md)
- [International draft field summary](assets/templates/fields-summary.md)
- [Scnet OCR API endpoint](https://api.scnet.cn/api/llm/v1/ocr/recognize)
- [Scnet service website](https://www.scnet.cn)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [JSON data on standard output, with text diagnostics for configuration, consent, network, API, and rate-limit errors.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SCNET_API_KEY and explicit upload confirmation; accepts only the INTERNATIONAL_BILL OCR type.]

## Skill Version(s):

0.1.2 (source: server release metadata; artifact frontmatter and changelog list 1.0.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
