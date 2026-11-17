## Description:

Recognizes payment voucher documents with Scnet OCR and extracts structured fields such as payer, payee, account details, amount, usage, signatures or stamps, and confidence data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scnet-sugon](https://clawhub.ai/user/scnet-sugon)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to submit authorized payment voucher images, PDFs, or archives to Scnet OCR and receive structured voucher fields for review, reconciliation, or downstream automation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends sensitive payment voucher files and an API token to a configurable external Scnet endpoint.

Mitigation: Use only payment documents approved for upload, verify SCNET_API_BASE is the intended HTTPS Scnet endpoint, and require explicit user approval before processing sensitive files.

Risk: The API key can be exposed if copied into chat or stored with broad file permissions.

Mitigation: Store SCNET_API_KEY in a protected environment or config file, keep config/.env restricted to the owner, and rotate the key if exposure is suspected.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/scnet-sugon/skills/payment-voucher-ocr)
- [Scnet website](https://www.scnet.cn)
- [Sugon-Scnet OCR API documentation summary](artifact/references/api-docs.md)
- [Payment voucher fields summary](artifact/assets/templates/fields-summary.md)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration guidance]

**Output Format:** [Structured JSON data on stdout, with human-readable error text on failure.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SCNET_API_KEY and a local file path; supports the WITHDRAWAL_VOUCHER OCR type.]

## Skill Version(s):

1.0.0 (source: frontmatter, skill.yaml, changelog, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
