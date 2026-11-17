## Description:

Use the oo CLI to search and read Rentman contacts, contact persons, equipment, and projects through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Rentman users can use this skill through the oo CLI to look up contacts, contact persons, equipment, and projects in an already connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First-time setup runs remote installation code whose exact changes were not established by the supplied evidence.

Mitigation: Review and approve CLI installation separately before running setup.

Risk: Rentman access is mediated through OOMOL, and the skill can automatically synchronize skills.

Mitigation: Review OOMOL's access role and the documented synchronization controls before use.

## Reference(s):

- [Rentman](https://rentman.io)
- [Rentman API documentation](https://api.rentman.net/)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [Rentman skill page](https://clawhub.ai/oomol/skills/oo-rentman)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [Structured Rentman data and concise text responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only lookup results for contacts, contact persons, equipment, and projects.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
