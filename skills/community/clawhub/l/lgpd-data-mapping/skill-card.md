## Description:

Build and maintain a canonical data inventory (mapa de dados) of all personal data processing activities, databases, APIs, cookies, pixels, mobile/web SDKs, telemetry streams, and third-party legal roles. Run FIRST before `lgpd-legal-basis`, `lgpd-ropa`, `lgpd-ripd`, and `lgpd-retention-erasure`. Produces `.lgpd/data-map.md`.

This skill is ready for commercial/non-commercial use.

## Publisher:

[goul4rt](https://clawhub.ai/user/goul4rt)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and privacy teams use this skill to map personal data processing across a project and prepare a preliminary inventory for legal-basis review, ROPA, RIPD, retention, and DSAR work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Security review has medium confidence and incomplete coverage because several referenced paths were not found in the scanned artifact.

Mitigation: Check the missing referenced paths against the full release before installing, especially if those paths matter to the intended use.

## Reference(s):

- [ClawHub release](https://clawhub.ai/goul4rt/skills/lgpd-data-mapping)
- [Server-resolved GitHub provenance](https://github.com/goul4rt/lgpd-skills/tree/main/skills/lgpd-data-mapping)

## Skill Output:

**Output Type(s):** [Markdown, Guidance]

**Output Format:** [Markdown personal data inventory in `.lgpd/data-map.md`; an optional Markdown draft can be extracted from Prisma annotations.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Project-specific inventory; greenfield work starts with a preliminary map.]

## Skill Version(s):

0.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
