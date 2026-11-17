## Description:

Greek tax compliance with AADE/TAXIS integration for VAT, payroll, EFKA, municipal taxes, and stamp duty, with human confirmation for all submissions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[satoshistackalotto](https://clawhub.ai/user/satoshistackalotto)

### License/Terms of Use:


## Use Case:

Accountants, finance teams, and developers use this skill to prepare Greek compliance outputs for VAT, payroll, EFKA, myDATA, TAXIS, municipal taxes, and filing deadline workflows. It supports offline preparation and requires human confirmation before government submissions.

### Deployment Geography for Use:

Greece

## Known Risks and Mitigations:

Risk: Sensitive AADE, EFKA, banking, payroll, or client data could be exposed if live credentials or taxpayer data are shared broadly.

Mitigation: Isolate submission credentials, keep credentials in environment variables, and do not expose live compliance data unless the workflow and access controls require it.

Risk: Government filings can create legal or financial consequences if prepared outputs are submitted without review.

Mitigation: Force each filing through implemented prepare, review, approve, and submit gates, with different preparer and approver identities before transmission.

Risk: Greek tax, payroll, and portal requirements may change after the skill content was authored.

Mitigation: Validate rates, deadlines, schemas, and submission requirements against current official sources before filing or advising a client.

Risk: Companion skill installation examples could pull unpinned or unreviewed dependencies into a compliance workflow.

Mitigation: Review companion skills before installation and pin trusted versions for production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/satoshistackalotto/skills/greek-compliance-aade)
- [AADE TAXIS portal](https://www1.aade.gr/taxisnet)
- [myDATA test endpoint](https://mydata-dev.azure-api.net)
- [myDATA production API](https://mydatapi.aade.gr)
- [EFKA portal](https://www.efka.gov.gr)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline command, XML, JSON, YAML, and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference local compliance files, environment variables, generated filing data, and human approval steps.]

## Skill Version(s):

0.1.2 (source: server release metadata; artifact frontmatter declares 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
