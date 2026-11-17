## Description:

Use a connected PartnerStack account to retrieve customer, deal, lead, and partnership data or create customers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

PartnerStack users can retrieve customer, deal, lead, and partnership records, and create customers through their connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The required CLI can change other agents’ installed skills without this skill explaining those effects.

Mitigation: Review the CLI separately before enabling the skill and limit automatic cross-agent skill changes; the publisher documents OO_SKILLS_SYNC_DISABLED=1 to disable startup synchronization.

Risk: An incorrect customer-creation payload could create unintended PartnerStack data.

Mitigation: Verify the exact customer-creation payload before approving the action.

Risk: The remote installers and hosted connector have not been audited.

Mitigation: Review the CLI separately before installation and consider the connector behavior unverified.

## Reference(s):

- [PartnerStack](https://partnerstack.com)
- [PartnerStack API documentation](https://docs.partnerstack.com/reference/auth)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Text responses and JSON data produced through shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read actions and customer creation; customer creation requires confirmation of the exact payload and effect.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
