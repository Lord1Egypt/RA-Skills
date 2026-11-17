## Description:

Validate Japanese Peppol e-invoices (JP PINT 1.1.3 UBL Invoice XML) with JPVerify against the official OASIS UBL 2.1 XSD and OpenPeppol JP PINT Schematron, optionally checking the seller's qualified-invoice T-number in the National Tax Agency registry.

This skill is ready for commercial/non-commercial use.

## Publisher:

[japanverify](https://clawhub.ai/user/japanverify)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and accounting teams use this skill to check Japanese JP PINT 1.1.3 UBL invoice XML before sending, accepting it into accounting, or paying it. It can also check the seller's qualified-invoice T-number in Japan's National Tax Agency registry.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan marks this release suspicious because complete invoice contents are sent to JPVerify without a clear privacy warning; the scan was partial, so its evidence is incomplete.

Mitigation: Before use, confirm that you are authorized to share the invoice under your privacy and business requirements, and send only data you are entitled to process and that the check needs.

## Reference(s):

- [JPVerify API key documentation](https://api.jpverify.com/docs/api-key)
- [JPVerify x402 documentation](https://api.jpverify.com/docs/x402)
- [JP PINT validation endpoint details](references/endpoints.md)
- [JP PINT request examples](references/examples.md)
- [Version 1.3.5 release notes](https://github.com/japanverify/jpverify-skills/releases/tag/v1.3.5)
- [ClawHub skill page](https://clawhub.ai/japanverify/skills/jp-pint-invoice-validation)

## Skill Output:

**Output Type(s):** [JSON, Guidance]

**Output Format:** [Structured validation result with document validity, rule-level findings, warnings, and optional registry evidence, summarized for the user.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Validation evidence only; not legal, tax, or Peppol conformance certification.]

## Skill Version(s):

1.3.5 (source: artifact/SKILL.md and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
