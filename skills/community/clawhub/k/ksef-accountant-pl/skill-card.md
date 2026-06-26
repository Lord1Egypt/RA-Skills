## Description: <br>
Polish-language accounting reference skill for KSeF 2.0, FA(3) invoices, VAT workflows, payment matching, correction invoices, split payment, JPK_V7 registers, and related accounting guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alexwoo-awso](https://clawhub.ai/user/alexwoo-awso) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Accountants, finance teams, and developers use this skill for Polish KSeF e-invoicing workflows, including API-oriented implementation guidance, FA(3) examples, VAT accounting flows, security patterns, and troubleshooting. It provides reference guidance and example patterns; users remain responsible for verifying legal, tax, banking, and production-system decisions. <br>

### Deployment Geography for Use: <br>
Poland <br>

## Known Risks and Mitigations: <br>
Risk: Financial and tax examples may be incomplete or out of date for a specific organization, transaction, or current Polish requirement. <br>
Mitigation: Verify MPP payment flows, FA(3) validation, accounting treatment, JPK_V7 handling, and legal conclusions with current Polish tax, accounting, and banking requirements before use. <br>
Risk: Production KSeF actions can create legally binding invoices or financial consequences. <br>
Mitigation: Test with the KSeF DEMO environment first and require explicit user approval before production submission, payment blocking, accounting-record changes, or other consequential actions. <br>
Risk: User-provided KSeF tokens, certificates, or encryption keys could be exposed if platform secret handling is not enforced. <br>
Mitigation: Use environment variables or a secrets manager, confirm secret isolation in the hosting platform, and do not paste credentials directly into agent conversations. <br>
Risk: The skill declares instruction-only and disabled autonomous invocation behavior, but enforcement depends on the hosting platform. <br>
Mitigation: Confirm registry metadata and platform controls before providing credentials or enabling production use; if controls are missing, use the skill only as unauthenticated reference documentation. <br>


## Reference(s): <br>
- [KSeF API 2.0 Reference](artifact/references/ksef-api-reference.md) <br>
- [Przyklady FA(3) XML](artifact/references/ksef-fa3-examples.md) <br>
- [Przeplywy Ksiegowe KSeF](artifact/references/ksef-accounting-workflows.md) <br>
- [Stan Prawny KSeF - Szczegoly](artifact/references/ksef-legal-status.md) <br>
- [Security & Compliance dla KSeF](artifact/references/ksef-security-compliance.md) <br>
- [Troubleshooting KSeF](artifact/references/ksef-troubleshooting.md) <br>
- [Funkcje AI dla KSeF](artifact/references/ksef-ai-features.md) <br>
- [Portal KSeF](https://ksef.podatki.gov.pl) <br>
- [KSeF API Documentation](https://ksef.mf.gov.pl/api/docs) <br>
- [API Bialej Listy VAT](https://wl-api.mf.gov.pl) <br>
- [KSeF Latarnia Status](https://github.com/CIRFMF/ksef-latarnia) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline code, XML, JSON, HTTP, SQL, and shell examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only reference output; examples require user review before use in real accounting or production KSeF systems.] <br>

## Skill Version(s): <br>
2.2.6 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
