## Description:

Know-your-business and e-invoice checks for EU counterparties in one call: official company registers, VAT (VIES) validation, sanctions screening and invoice format rules.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nutshell2000](https://clawhub.ai/user/nutshell2000)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to check whether EU counterparties exist, validate VAT details, screen for sanctions, and assess e-invoice formats before processing transactions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The unpinned `agentcash@latest` command can change without review, including for paid requests.

Mitigation: Use a reviewed, pinned agentcash version and review version changes before making paid calls.

Risk: Company identifiers are sent to Glyphcall when using its checks.

Mitigation: Review what identifiers will be sent and confirm they may be shared with Glyphcall before making a request.

## Reference(s):

- [Eu Company Check on ClawHub](https://clawhub.ai/nutshell2000/skills/glyphcall-eu-company)
- [Glyphcall KYB bundle API](https://api.glyphcall.com/pack/kyb-eu)
- [Glyphcall VAT validation API](https://api.glyphcall.com/vat/validate)
- [Glyphcall e-invoice check API](https://api.glyphcall.com/pack/einvoice-check)
- [Glyphcall sanctions screening API](https://api.glyphcall.com/sanctions/check)

## Skill Output:

**Output Type(s):** [Shell commands, API calls, Guidance]

**Output Format:** [Markdown with inline shell commands and API endpoint examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [API calls are pay-per-success; stated prices range from $0.01 to $0.02 per call.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
