## Description:

Booqable (booqable.com). Use this skill for ANY Booqable request — searching and reading data. Whenever a task involves Booqable, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

People working with a Booqable account can use the skill to find and read company, customer, order, and product group data through their connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: CLI setup may execute downloaded code without a separate approval or integrity check.

Mitigation: Review setup before allowing requests, use a pinned independently verified installation, and check which agent skills it installs or updates.

Risk: The connected service mediates access to Booqable business data, while the hosted service implementation has not been independently verified.

Mitigation: Connect only the account and permissions needed for the task.

## Reference(s):

- [Booqable](https://www.booqable.com/)
- [Booqable API documentation](https://developers.booqable.com/)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [API Calls, Text, Guidance]

**Output Format:** [JSON connector requests and returned data, with natural language summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only company, customer, order, and product group operations.]

## Skill Version(s):

1.0.6 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
