## Description:

Search and read Eventzilla organizer, event, attendee, ticket, transaction, and user data through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers with an OOMOL-connected Eventzilla account can retrieve the events and organizer records available to that account, including attendee, ticket, and transaction data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First-time setup directs users to run remote installers that were not verified.

Mitigation: Review setup instructions, approve software installation separately, and use a verified oo CLI release.

Risk: Authorized Eventzilla records pass through OOMOL.

Mitigation: Use only an Eventzilla account and records approved for the OOMOL connection, and review or disable automatic skill synchronization.

## Reference(s):

- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [Eventzilla](https://www.eventzilla.net)
- [Eventzilla API documentation](https://developer.eventzilla.net/docs/)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Text]

**Output Format:** [JSON records returned as text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Records are limited to those available to the connected Eventzilla organizer account.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
