## Description:

Polish-language accounting assistant for KSeF 2.0, FA(3) invoices, VAT/JPK workflows, payment matching, correcting invoices, split payment, security patterns, and related accounting guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alexwoo-awso](https://clawhub.ai/user/alexwoo-awso)

### License/Terms of Use:

MIT

## Use Case:

Accountants, finance teams, and developers use this skill to work with Polish KSeF e-invoicing flows, including KSeF API usage, FA(3) XML examples, VAT registers, JPK_V7 preparation, payment matching, corrections, and implementation-oriented security/compliance patterns.

### Deployment Geography for Use:

Poland

## Known Risks and Mitigations:

Risk: Sensitive KSeF credentials could be exposed or misused if platform secret handling or disable-model-invocation controls are not enforced.

Mitigation: Do not provide production KSeF tokens, encryption keys, or certificates unless the platform confirms secret isolation and disable-model-invocation enforcement.

Risk: Accounting examples include actions with financial or legal impact, including sending invoices, posting accounting entries, holding payments, and production KSeF use.

Mitigation: Require explicit human approval before financial, tax, payment, or production KSeF actions, and test with the demo environment before production use.

Risk: Troubleshooting material suggests running an external GitHub status script.

Mitigation: Pin, review, and approve any external code before running it; do not execute cloned scripts directly in a sensitive financial environment.

Risk: Incorrect XML validation or weak exported register storage could create compliance, audit, or data integrity issues.

Mitigation: Validate FA(3) XML against current official schemas and harden storage, access control, audit logging, and retention before production deployment.

## Reference(s):

- [KSeF API Reference](references/ksef-api-reference.md)
- [FA(3) XML Examples](references/ksef-fa3-examples.md)
- [KSeF Accounting Workflows](references/ksef-accounting-workflows.md)
- [KSeF AI Features](references/ksef-ai-features.md)
- [KSeF Security and Compliance](references/ksef-security-compliance.md)
- [KSeF Legal Status](references/ksef-legal-status.md)
- [KSeF Troubleshooting](references/ksef-troubleshooting.md)
- [Official KSeF Portal](https://ksef.podatki.gov.pl)
- [KSeF API Documentation](https://ksef.mf.gov.pl/api/docs)
- [KSeF Demo Environment](https://ksef-demo.mf.gov.pl)
- [KSeF Production Environment](https://ksef.mf.gov.pl)
- [VAT White List API](https://wl-api.mf.gov.pl)
- [KSeF Latarnia Status Tool](https://github.com/CIRFMF/ksef-latarnia)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with code snippets, XML and JSON examples, workflow checklists, and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Instruction-only; examples are reference material for user implementation and do not run as skill code.]

## Skill Version(s):

2.2.6 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
