## Description:

Implement endpoints and operational workflows for data subject rights (DSAR) under LGPD Arts. 18, 19, and 20, distinguishing standard controller SLAs (immediate simplified / 15d complete) from ATPP SLAs under Resolução CD/ANPD nº 2/2022 Art. 14 (15d simplified / 30d complete). Covers legal representatives, ex-employees, informal channels, and proportional identity verification. Outputs `.lgpd/dsar/workflow.md` + endpoint specs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[goul4rt](https://clawhub.ai/user/goul4rt)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and privacy teams can use this skill to design and document LGPD data subject request workflows, response deadlines, identity checks, and related service endpoints. It provides operational guidance and implementation examples for handling access, correction, portability, erasure, consent revocation, and automated-decision review requests.

### Deployment Geography for Use:

Brazil

## Known Risks and Mitigations:

Risk: Some referenced materials were only partly inspected, so the scan does not establish that every part of the skill was fully assessed.

Mitigation: Review the referenced materials before relying on the guidance or deploying an implementation.

Risk: The skill also references broader child and adolescent compliance material that may not fit every organization's needs.

Mitigation: Confirm that the related child and adolescent compliance guidance is relevant to the organization's use case.

## Reference(s):

- [Server-resolved source repository](https://github.com/goul4rt/lgpd-skills/tree/main/skills/lgpd-dsar)
- [ClawHub release page](https://clawhub.ai/goul4rt/skills/lgpd-dsar)
- [Endpoint implementation examples](assets/endpoints.md)
- [DSAR SLA and erasure disposition examples](assets/dsar-sla.ts)

## Skill Output:

**Output Type(s):** [Markdown, Code, Guidance]

**Output Format:** [Markdown workflow documentation and endpoint specifications with TypeScript examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Examples and operational guidance for LGPD DSAR workflows; legal applicability should be reviewed for the specific organization and request.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
