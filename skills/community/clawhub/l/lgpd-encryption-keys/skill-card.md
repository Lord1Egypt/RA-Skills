## Description:

Configure encryption in transit, cloud storage/volume encryption at rest, application-level column encryption, blind indexing, and KMS key management as engineering controls aligned with LGPD Art. 46 and ANPD's Information Security Guide. Outputs tested AES-256-GCM + Prisma query extension handlers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[goul4rt](https://clawhub.ai/user/goul4rt)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to configure transport, infrastructure, and application-level encryption and key management for systems processing personal data, informed by LGPD Art. 46 and ANPD guidance.

### Deployment Geography for Use:

Brazil (LGPD and ANPD guidance context)

## Known Risks and Mitigations:

Risk: The skill includes executable TypeScript that handles encryption keys; the scanner classified its credential-access alert as expected and reported a benign verdict.

Mitigation: Review the implementation before adoption, keep keys in an approved KMS or secret store, and restrict runtime access to them.

Risk: The Prisma handlers do not automatically cover raw SQL queries or nested writes, which can bypass the documented encryption and decryption paths.

Mitigation: Encrypt and decrypt those paths explicitly or route them through a service that applies the handlers, and document the coverage for the application.

## Reference(s):

- [Server-resolved source repository](https://github.com/goul4rt/lgpd-skills/tree/main/skills/lgpd-encryption-keys)
- [ClawHub skill page](https://clawhub.ai/goul4rt/skills/lgpd-encryption-keys)
- [Field encryption reference implementation](artifact/assets/field-encryption.ts)

## Skill Output:

**Output Type(s):** [Guidance, Code, Configuration]

**Output Format:** [Markdown guidance with TypeScript reference code and Prisma configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes a reference implementation for AES-256-GCM field encryption and Prisma handlers; adapt configuration and coverage to the application.]

## Skill Version(s):

0.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
