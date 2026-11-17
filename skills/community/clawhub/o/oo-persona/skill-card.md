## Description:

Use Persona through an OOMOL-connected account to read, create, and update Persona inquiries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to read and manage Persona inquiries through their connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may execute unverified oo CLI installer code and introduce persistent skill changes for other agents.

Mitigation: Review and install a verified CLI release separately; check automatic skill installation behavior and use OO_SKILLS_SYNC_DISABLED to control startup synchronization when appropriate.

Risk: Persona requests are processed by OOMOL through the connected account, and create or update actions change data.

Mitigation: Connect only the intended Persona account and retain confirmation before changes.

## Reference(s):

- [Persona](https://withpersona.com/)
- [Persona API reference](https://docs.withpersona.com/api-reference/)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Guidance]

**Output Format:** [JSON connector results and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Create and update actions change Persona data and require confirmation.]

## Skill Version(s):

1.0.4 (source: frontmatter and release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
