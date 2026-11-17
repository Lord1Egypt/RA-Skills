## Description:

Operate 7shifts through an OOMOL-connected account to retrieve companies, departments, locations, roles, users, and account identity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External operators use the skill to search and read 7shifts company, department, location, role, user, and account identity data through a connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup fallback can run remote installers and may install or update agent skills without those changes being disclosed.

Mitigation: Review the CLI installation separately, use a reviewed release, inspect which skills it installs or updates, and disable automatic skill synchronization if unwanted.

Risk: Connector requests are processed by OOMOL, and broad 7shifts access may expose more account data than the task needs.

Mitigation: Connect only the necessary 7shifts permissions and account for OOMOL processing the requests.

## Reference(s):

- [7shifts API documentation](https://developers.7shifts.com/)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)
- [7shifts](https://www.7shifts.com/)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [JSON connector data with concise text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only company and account data]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
