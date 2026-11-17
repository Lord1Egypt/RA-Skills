## Description:

Config-driven PromoStandards client for supplier SOAP services including inventory, product data, pricing and configuration, and purchase-order submission.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zmtucker](https://clawhub.ai/user/zmtucker)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and procurement agents use this skill to query PromoStandards supplier capabilities, inventory, product, pricing, and ordering data, and to submit purchase orders when appropriate supplier credentials and safe endpoints are configured.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Supplier credentials and business data may be sent to externally configured SOAP endpoints.

Mitigation: Install only where callers and supplier configuration are trusted, prefer bundled registry or administrator-reviewed configs, and block inline configJson from untrusted users.

Risk: Externally configured destinations may use unsafe or plaintext endpoints.

Mitigation: Reject or override plaintext HTTP endpoints and review supplier endpoint configuration before deployment.

Risk: Purchase-order submission can create production business effects.

Mitigation: Use preview-po and supplier test endpoints before production order submission, and bind least-privilege supplier credentials.

## Reference(s):

- [PromoStandards](https://promostandards.org)
- [ClawHub Skill Page](https://clawhub.ai/zmtucker/skills/promostandards)
- [Publisher Profile](https://clawhub.ai/user/zmtucker)
- [Registry Findings](artifact/references/registry_findings.md)
- [Adding a Supplier](artifact/references/adding_a_supplier.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash examples and JSON command output from the bundled CLI tools]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call external supplier SOAP endpoints; purchase-order submission is write-capable and should be previewed or directed to test endpoints before production use.]

## Skill Version(s):

0.3.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
