## Description:

Design and implement tamper-evident, transactionally serialized audit logging as a recommended engineering control for LGPD accountability (Art. 6, X) and security (Art. 46). Outputs Prisma schema, concurrency-safe hash-chain writer, DB write-protection triggers, and external WORM/SIEM anchoring verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[goul4rt](https://clawhub.ai/user/goul4rt)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to design LGPD-oriented audit logging for accountability and security, including chained records, database protections, and external integrity checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan rates this release suspicious because reported weaknesses could make its audit trail unreliable or allow records to be altered without detection.

Mitigation: Postpone installation until the integrity protections and concurrent-write behavior have been reviewed and corrected.

Risk: Skillspector reports partial coverage (33.3%; two files partly inspected), so the scan cannot establish that unreported behavior is safe.

Mitigation: Review the remaining behavior before installation; do not treat the partial scan as evidence that unreported behavior is safe.

## Reference(s):

- [Reference Prisma schema](assets/audit-log.prisma)
- [Reference TypeScript implementation](assets/audit-log.ts)
- [Source repository (server-resolved provenance)](https://github.com/goul4rt/lgpd-skills/tree/main/skills/lgpd-audit-logging)
- [ClawHub skill page](https://clawhub.ai/goul4rt/skills/lgpd-audit-logging)

## Skill Output:

**Output Type(s):** [Code, Configuration instructions, Guidance]

**Output Format:** [Markdown guidance with TypeScript code and a Prisma schema]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes reference implementation files and recommendations for audit-trail integrity checks.]

## Skill Version(s):

0.1.0 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
