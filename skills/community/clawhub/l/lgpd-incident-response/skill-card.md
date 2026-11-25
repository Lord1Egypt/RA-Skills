## Description:

Guides agents through LGPD security incident triage, containment, notification, and recordkeeping in emergency and preparation workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[goul4rt](https://clawhub.ai/user/goul4rt)

### License/Terms of Use:

MIT-0

## Use Case:

Brazilian privacy, security, and legal response teams use the skill to coordinate incident triage, containment, notification decisions, and incident records under the LGPD and ANPD Resolution 15/2024. It provides emergency and audit-preparation workflows with draft notices for the ANPD and affected people.

### Deployment Geography for Use:

Brazil

## Known Risks and Mitigations:

Risk: Containment actions such as revoking credentials or isolating resources may disrupt affected services.

Mitigation: Check the incident-response process and expected service impact before applying containment steps.

Risk: Scan coverage is incomplete because some referenced local paths were not found in the bundle.

Mitigation: Confirm required referenced files are present in the deployment package before relying on them.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/goul4rt/skills/lgpd-incident-response)
- [Source repository (server-resolved provenance)](https://github.com/goul4rt/lgpd-skills/tree/main/skills/lgpd-incident-response)

## Skill Output:

**Output Type(s):** [Guidance, Markdown]

**Output Format:** [Markdown runbook guidance, notification templates, and incident-log examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Emergency and preparation workflows; triage and notification decisions include human and legal review checkpoints.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
