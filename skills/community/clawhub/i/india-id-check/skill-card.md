## Description:

Validate, identify, mask and redact Indian identifiers offline - Aadhaar (Verhoeff check digit), PAN, GSTIN, TAN, IFSC, UPI ID, mobile, PIN code, vehicle number (incl. BH series and TG/TS), driving licence, passport, voter ID, CIN, LLPIN, Udyam and card numbers. Use when checking form inputs or KYC data, decoding what an Indian ID means, masking Aadhaar/PAN for display, or removing personal data from text before storing or sharing it.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sanketbhatia](https://clawhub.ai/user/sanketbhatia)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and KYC or form operators can use this skill to validate and decode Indian identifiers, compare related fields, and mask or redact sensitive values before sharing or storing text. Offline checks help catch format and checksum errors; a valid result does not establish that an identifier is real or belongs to a person.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: IFSC and PIN lookup commands send supplied values to third-party services.

Mitigation: Use lookup only when branch or post-office details are needed and you are comfortable sending the supplied value to the named external service.

Risk: Redaction coverage may not include every advertised identifier type, and the security review was partial.

Mitigation: Check that the needed identifier types are covered and inspect redacted output before storing or sharing sensitive text.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/sanketbhatia/skills/india-id-check)
- [Publisher profile](https://clawhub.ai/user/sanketbhatia)

## Skill Output:

**Output Type(s):** [JSON, Text, Guidance]

**Output Format:** [JSON validation results with concise text summaries, masked values, or redacted text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Sensitive Aadhaar and card values are hidden or masked in relevant outputs; format validity is not identity verification.]

## Skill Version(s):

1.0.0 (source: frontmatter, ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
