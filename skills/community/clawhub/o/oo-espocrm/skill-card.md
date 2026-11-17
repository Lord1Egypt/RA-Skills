## Description:

Use EspoCRM to read, create, update, and delete CRM records through the connected OOMOL account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

People working with EspoCRM can use this skill to retrieve CRM records and metadata or to create, update, and delete records through their connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: CLI setup may execute unverified remote code.

Mitigation: Review and approve CLI installation separately, and prefer a verified, fixed release.

Risk: Setup may introduce agent-skill changes that are not explained by the skill.

Mitigation: Decide whether skill synchronization is allowed; the publisher documents OO_SKILLS_SYNC_DISABLED=1 to prevent startup synchronization.

Risk: CRM write and delete actions can change or remove records.

Mitigation: Use narrowly scoped CRM credentials and retain confirmation of the target, payload, and effect.

## Reference(s):

- [EspoCRM API documentation](https://docs.espocrm.com/development/api/)
- [EspoCRM](https://www.espocrm.com/)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Text]

**Output Format:** [Structured CRM data and natural-language summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can read records or make CRM changes; write and delete actions require confirmation.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
