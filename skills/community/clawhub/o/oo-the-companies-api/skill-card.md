## Description:

Use The Companies API to read, search, and update company data through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to count or search companies and retrieve company data by domain, email, or social profile through a connected account. It also documents when an action can update provider data and requires confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Initial CLI setup can run downloaded code, and automatic skill synchronization can introduce broader agent changes.

Mitigation: Verify the release before installation and consider disabling automatic skill synchronization.

Risk: The external connector implementation was not verified, and OOMOL receives requested API inputs while mediating connected-account access.

Mitigation: Send only the inputs needed for the requested action, review the connected account, and retain confirmation for state-changing actions.

## Reference(s):

- [The Companies API documentation](https://www.thecompaniesapi.com/api/get-started)
- [The Companies API homepage](https://www.thecompaniesapi.com)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Guidance]

**Output Format:** [JSON API responses and shell commands documented in Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses may include company data and pagination metadata.]

## Skill Version(s):

1.0.2 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
