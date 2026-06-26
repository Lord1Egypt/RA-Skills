## Description: <br>
Provides English guidance for Polish KSeF 2.0 accounting workflows, including FA(3) invoices, VAT compliance, e-invoice processing, payment matching, corrective invoices, and security patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alexwoo-awso](https://clawhub.ai/user/alexwoo-awso) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Accountants, finance teams, and developers use this skill as an English reference for working with Poland's National e-Invoice System, including KSeF API operations, FA(3) invoice structures, VAT registers, payment matching, corrections, and secure implementation patterns. <br>

### Deployment Geography for Use: <br>
Poland <br>

## Known Risks and Mitigations: <br>
Risk: The skill discusses sensitive accounting, VAT, invoice, payment, and production KSeF workflows. <br>
Mitigation: Use demo KSeF endpoints for testing and require human accounting review before any production invoice, payment, VAT, or record-changing action. <br>
Risk: KSeF tokens, certificates, and encryption keys could be exposed if the hosting platform does not protect declared secrets. <br>
Mitigation: Configure production credentials only through protected secret storage after verifying environment variable isolation; never paste credentials into the conversation. <br>
Risk: Instruction-only and manual-invocation flags depend on platform enforcement. <br>
Mitigation: Install as a reference skill, verify registry metadata before use, and do not grant autonomous or credentialed access when those flags are not enforced. <br>
Risk: Legal and tax requirements may change after the skill content was authored. <br>
Mitigation: Check current official KSeF and Polish tax guidance and consult a qualified tax advisor before production use. <br>


## Reference(s): <br>
- [KSeF Accountant En on ClawHub](https://clawhub.ai/alexwoo-awso/ksef-accountant-en) <br>
- [KSeF API 2.0 Reference](references/ksef-api-reference.md) <br>
- [KSeF Legal Status - Details](references/ksef-legal-status.md) <br>
- [FA(3) XML Examples](references/ksef-fa3-examples.md) <br>
- [KSeF Accounting Workflows](references/ksef-accounting-workflows.md) <br>
- [AI Features for KSeF](references/ksef-ai-features.md) <br>
- [Security & Compliance for KSeF](references/ksef-security-compliance.md) <br>
- [KSeF Troubleshooting](references/ksef-troubleshooting.md) <br>
- [KSeF Portal](https://ksef.podatki.gov.pl) <br>
- [KSeF DEMO](https://ksef-demo.mf.gov.pl) <br>
- [KSeF Production](https://ksef.mf.gov.pl) <br>
- [VAT White List API](https://wl-api.mf.gov.pl) <br>
- [KSeF Latarnia Status](https://github.com/CIRFMF/ksef-latarnia) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with code, XML, JSON, and HTTP examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only; examples are illustrative and require user review before production use.] <br>

## Skill Version(s): <br>
2.2.6 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
