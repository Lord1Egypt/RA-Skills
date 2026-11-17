## Description:

Search and read Fidel API brands, cards, and transactions through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to retrieve brands, cards, and transactions from the Fidel account connected through OOMOL.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First-time setup may run an unverified remote installer without a separate approval step; the hosted connector implementation is also unverified and mediates sensitive card and transaction requests.

Mitigation: Review setup, install a verified and pinned CLI separately, consider disabling automatic skill synchronization, and connect only the Fidel account needed for the task.

## Reference(s):

- [Fidel API documentation](https://reference.fidel.uk/)
- [Fidel API](https://fidel.uk)
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API data, JSON, Guidance]

**Output Format:** [JSON API responses and Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only Fidel brand, card, and transaction data.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
