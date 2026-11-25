## Description:

Define data retention schedules, post-contract minimization, logical blocking, backup/replica erasure strategies, and operator propagation under LGPD Arts. 15, 16, and 18 (VI and § 6). Outputs precise Brazilian statutory retention references (document, legal basis, timeframe, dies a quo) and Prisma retention/outbox schemas.

This skill is ready for commercial/non-commercial use.

## Publisher:

[goul4rt](https://clawhub.ai/user/goul4rt)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and privacy teams use this skill to define record-specific retention and deletion rules for Brazilian systems, plan erasure across databases, backups, and service operators, and create Prisma schemas for retention and propagation workflows.

### Deployment Geography for Use:

Brazil

## Known Risks and Mitigations:

Risk: The security assessment has medium confidence because one referenced local path was unresolved, leaving the scan evidence incomplete.

Mitigation: Resolve the referenced path and review its contents before installing.

Risk: Retention rules depend on the record type, applicable legal basis, counting start event, and regulated sector.

Mitigation: Map rules to specific records and have Brazilian counsel validate which requirements apply to the project.

## Reference(s):

- [Server-resolved source repository](https://github.com/goul4rt/lgpd-skills/tree/main/skills/lgpd-retention-erasure)
- [ClawHub skill release](https://clawhub.ai/goul4rt/skills/lgpd-retention-erasure)
- [Retention Prisma schema](artifact/assets/retention.prisma)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Configuration]

**Output Format:** [Markdown guidance and Prisma schema examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes record-specific legal bases, retention periods, and counting start events.]

## Skill Version(s):

0.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
