## Description:

Read Precoro catalog items, purchase orders, suppliers, users, and warehouses through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Procurement teams use this skill to look up Precoro catalog, purchase order, supplier, user, and warehouse information through their connected OOMOL account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic CLI setup may execute unverified software, and automatic skill synchronization may make undisclosed changes to other agents.

Mitigation: Review and explicitly approve CLI setup, preferably installing a verified version yourself. Review or disable automatic synchronization using the documented controls; the downloaded installers were unavailable for inspection.

## Reference(s):

- [Precoro API documentation](https://help.precoro.com/using-api-in-precoro)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [oo CLI synchronization controls](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md)
- [Precoro](https://precoro.com/)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Text]

**Output Format:** [JSON data with natural-language summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only Precoro information available to the connected account.]

## Skill Version(s):

1.0.5 (source: frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
