## Description:

Organises accounting documents for French accounting firms by classifying invoices and bank statements into client, year, month, and document-type folders, then reporting any items that need accountant review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[trendex](https://clawhub.ai/user/trendex)

### License/Terms of Use:

MIT-0

## Use Case:

Accountants and firm staff use this skill to sort incoming accounting documents, maintain client document indexes, and surface ambiguous or incomplete items for human review.

### Deployment Geography for Use:

France

## Known Risks and Mitigations:

Risk: The skill is intended to process sensitive accounting documents automatically.

Mitigation: Require explicit opt-in before unattended email or file processing and constrain the skill to a known inbox and client root.

Risk: The skill writes long-lived local document copies and indexes.

Mitigation: Review retention expectations, access controls, output locations, and audit or rollback procedures before deployment.

Risk: Company lookup may contact an external public company-data service.

Mitigation: Disable or document external lookup behavior when confidential workflows must remain fully local.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/trendex/skills/organisation-documents)
- [Reference - Invocation contract and sources](references/contrat-io.md)
- [Reference - Target structure and naming conventions](references/structure-cible.md)
- [Reference - French accounting extraction and validation](references/validation-fr.md)
- [Reference - 2026 electronic invoicing reform](references/reforme-facturation-2026.md)
- [Reference - Tools, success criteria, and roadmap](references/roadmap.md)
- [Annuaire des Entreprises API](https://annuaire-entreprises.data.gouv.fr/api)
- [Companion bank reconciliation skill](https://github.com/developers-trendex/rapprochement-bancaire)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Plain-language summary with JSON report data and shell command usage]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local document copies, clients.json, _index.json, _report.json, and follow-up questions for accountant review.]

## Skill Version(s):

0.2.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
