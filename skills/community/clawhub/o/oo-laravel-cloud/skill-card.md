## Description:

Laravel Cloud (cloud.laravel.com). Use this skill for ANY Laravel Cloud request — searching and reading data. Whenever a task involves Laravel Cloud, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use it to search and read the connected Laravel Cloud organization's applications, environments, deployments, and available regions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup fallback runs an unverified remote installer, and its local changes are not clearly controlled.

Mitigation: Review and approve CLI installation separately. Check whether the chosen CLI release installs or updates other agent skills, and disable that behavior if unwanted. Grant only the Laravel Cloud permissions needed and account for OOMOL-mediated access.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/oomol/skills/oo-laravel-cloud)
- [Laravel Cloud](https://cloud.laravel.com)
- [Laravel Cloud API authentication documentation](https://cloud.laravel.com/docs/api/authentication)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [Text, Structured data, Guidance]

**Output Format:** [Text summaries and structured data from Laravel Cloud queries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Account-specific results depend on the connected Laravel Cloud organization and permissions.]

## Skill Version(s):

1.0.4 (source: frontmatter, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
