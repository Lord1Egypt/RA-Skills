## Description:

Design an event-sourced, database-enforced append-only consent ledger satisfying LGPD Art. 8 (free, informed, unambiguous consent, burden of proof, easy revocation, policy version supersession), Art. 14, and Art. 18, IX. Use when user asks for "consent schema", "consent ledger", "schema de consentimento", "Prisma consentimento", or integrates consent capture/revocation with Better Auth, NextAuth, or Clerk. Outputs Prisma schema, PostgreSQL append-only triggers, and TypeScript helpers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[goul4rt](https://clawhub.ai/user/goul4rt)

### License/Terms of Use:

MIT-0

## Use Case:

Developers building applications that rely on consent as a legal basis can use this skill to model an auditable consent ledger, record grants and revocations, and check current consent before processing. Its examples cover Brazilian LGPD requirements and Prisma, PostgreSQL, and TypeScript implementations.

### Deployment Geography for Use:

Brazil

## Known Risks and Mitigations:

Risk: The examples collect request metadata such as IP address and user agent, which may not fit every application's privacy expectations.

Mitigation: Tell users what request metadata is collected, and minimize collection to what the consent record needs.

Risk: Security analysis is incomplete because a local reference was missing, so the full behavior was not assessed.

Mitigation: Resolve and review the missing reference before relying on the skill in an application.

## Reference(s):

- [Source repository and skill path](https://github.com/goul4rt/lgpd-skills/tree/main/skills/lgpd-consent-schema)
- [ClawHub skill release](https://clawhub.ai/goul4rt/skills/lgpd-consent-schema)

## Skill Output:

**Output Type(s):** [Code, Configuration instructions, Guidance]

**Output Format:** [Markdown with Prisma, SQL, and TypeScript code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reusable schema, database trigger, and typed helper examples]

## Skill Version(s):

0.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
