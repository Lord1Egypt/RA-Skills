## Description:

Produce a Relatório de Impacto à Proteção de Dados Pessoais (RIPD / DPIA) under LGPD Art. 38, applying the cumulative high-risk test of Resolução CD/ANPD nº 2/2022 Art. 4 (multifactorial large scale + specific criteria) or precautionary risk governance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[goul4rt](https://clawhub.ai/user/goul4rt)

### License/Terms of Use:

MIT-0

## Use Case:

Privacy, legal, DPO, and engineering teams use the skill to draft an LGPD RIPD from a project's data map, document privacy risks and safeguards, and prepare the report for human, legal, and DPO review.

### Deployment Geography for Use:

Brazil

## Known Risks and Mitigations:

Risk: The security review is partial because the referenced `.lgpd/data-map.md` was unavailable, so the assessment may omit project-specific processing activities.

Mitigation: Confirm the data map is present and review it before relying on the resulting RIPD.

Risk: A generated RIPD may contain incomplete or misleading legal or privacy analysis if project facts or regulatory guidance are inaccurate or outdated.

Mitigation: Follow the skill's required human, legal, and DPO review checkpoint before approving the report.

## Reference(s):

- [Server-resolved source: goul4rt/lgpd-skills (skills/lgpd-ripd)](https://github.com/goul4rt/lgpd-skills/tree/main/skills/lgpd-ripd)
- [ClawHub skill release](https://clawhub.ai/goul4rt/skills/lgpd-ripd)
- [Publisher profile: goul4rt](https://clawhub.ai/user/goul4rt)
- [RIPD report template](assets/ripd-template.md)

## Skill Output:

**Output Type(s):** [Markdown, Guidance]

**Output Format:** [Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates `.lgpd/RIPD/ripd-{slug}.md` from a report template and requires human, legal, and DPO review before approval.]

## Skill Version(s):

0.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
