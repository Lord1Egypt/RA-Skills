## Description:

National e-Invoice System (KSeF) accounting assistant in English for KSeF 2.0 API work, FA(3) invoices, Polish VAT compliance, e-invoice processing, payment matching, VAT registers, corrective invoices, split payment, and related accounting workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alexwoo-awso](https://clawhub.ai/user/alexwoo-awso)

### License/Terms of Use:

MIT

## Use Case:

Accountants, tax operations staff, and developers use this skill for English-language guidance on Polish KSeF 2.0 workflows, FA(3) invoice handling, VAT registers, payment matching, corrective invoices, and implementation patterns around KSeF integrations.

### Deployment Geography for Use:

Poland

## Known Risks and Mitigations:

Risk: The security scan reports unsafe automated accounting posting examples and unpinned remote code examples.

Mitigation: Require human approval before invoice submission, payment blocking, or accounting posting, and pin and verify any external script source before running it.

Risk: Production KSeF tokens or encryption keys could be exposed if platform secret isolation or autonomous-invocation controls are not enforced.

Mitigation: Do not provide production credentials until the platform confirms secret isolation and disabled autonomous invocation; use demo endpoints for testing.

Risk: KSeF, VAT, and tax guidance can become outdated or be misapplied to binding financial decisions.

Mitigation: Verify current Polish Ministry of Finance guidance and consult qualified tax advisors before production use or legal compliance decisions.

## Reference(s):

- [KSeF Accounting Workflows](references/ksef-accounting-workflows.md)
- [AI Features for KSeF](references/ksef-ai-features.md)
- [KSeF API 2.0 Reference](references/ksef-api-reference.md)
- [FA(3) XML Examples](references/ksef-fa3-examples.md)
- [KSeF Legal Status Details](references/ksef-legal-status.md)
- [Security & Compliance for KSeF](references/ksef-security-compliance.md)
- [KSeF Troubleshooting](references/ksef-troubleshooting.md)
- [KSeF Portal](https://ksef.podatki.gov.pl)
- [KSeF Demo API](https://ksef-demo.mf.gov.pl)
- [KSeF Production API](https://ksef.mf.gov.pl)
- [VAT White List API](https://wl-api.mf.gov.pl)
- [KSeF Latarnia Status](https://github.com/CIRFMF/ksef-latarnia)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown with illustrative code, XML, JSON, HTTP, and shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Instruction-only; examples are for user implementation and require human review before production or financial action.]

## Skill Version(s):

2.2.6 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
