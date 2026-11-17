## Description:

Search and read customer and order data from a connected Snipcart account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and store operators use the connected Snipcart account to search and retrieve customer records and completed order details. The skill supports read-only customer and order lookups, lists, pagination, and filters.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Initial setup may install and execute an unverified CLI without a separate approval step.

Mitigation: Review and approve CLI installation separately, and prefer a verified, fixed release. Disable startup skill synchronization with OO_SKILLS_SYNC_DISABLED=1 if it is not needed.

Risk: Using the connected account exposes customer and order data through OOMOL-mediated access.

Mitigation: Connect only the intended Snipcart account and limit use to the customer or order data needed for the task.

## Reference(s):

- [Snipcart API Reference](https://docs.snipcart.com/v3/api-reference/introduction)
- [Snipcart](https://snipcart.com/)
- [oo CLI Repository](https://github.com/oomol-lab/oo-cli)
- [oo CLI Installation Guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [API data, JSON, Text summaries]

**Output Format:** [JSON records and concise text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only customer and completed-order results, with pagination and optional filters.]

## Skill Version(s):

1.0.6 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
