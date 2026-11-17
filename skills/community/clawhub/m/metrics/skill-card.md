## Description:

Capture, normalize, and report metrics across any domain with reusable dimensions, programmable formulas, and scalable reporting workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

Employees, external users, and developers use this skill to define metric contracts, govern formulas, build decision-oriented reports, and maintain reusable alerting workflows across business, product, marketing, operations, finance, and personal domains.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persisted metric context could include confidential raw business data, secrets, credentials, or unrelated personal details if users add them to local memory.

Mitigation: Store only metric definitions, decisions, formulas, owners, and report cadence notes; avoid storing secrets, credentials, raw business records, or unrelated personal data.

Risk: Formula changes or ambiguous metric contracts can make reports misleading or break historical comparability.

Mitigation: Require explicit metric contracts, version every formula change, document impact expectations, and block report publication when critical quality checks fail.

Risk: Automated alerts can create noise or prompt the wrong response when thresholds lack ownership and escalation rules.

Mitigation: Use explicit trigger conditions, severity levels, owners, response playbooks, cooldown windows, and regular threshold reviews.

## Reference(s):

- [Metrics Skill Page](https://clawhub.ai/ivangdavila/skills/metrics)
- [Metrics Homepage](https://clawic.com/skills/metrics)
- [Setup - Metrics](artifact/setup.md)
- [Memory Template - Metrics](artifact/memory-template.md)
- [Metric Registry Guide](artifact/metric-registry.md)
- [Formula Playbook](artifact/formula-playbook.md)
- [Reporting Pack](artifact/reporting-pack.md)
- [Automation Patterns](artifact/automation-patterns.md)
- [Data Quality Gates](artifact/data-quality.md)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown guidance, templates, metric definitions, formula specifications, report outlines, and alert policy drafts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local metrics memory under ~/metrics/ when the user enables persistence.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
