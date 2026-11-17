## Description:

Search and read Ghost site content through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Ghost site users and developers can retrieve published posts and pages, public authors and tags, and site settings from a connected Ghost site.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First-time setup can run downloaded installer code whose payload and system changes have not been verified.

Mitigation: Review setup behavior, install a verified oo CLI release yourself, and require approval before any downloaded installer runs.

Risk: Connecting a Ghost account uses OOMOL-managed credentials and may involve usage charges.

Mitigation: Connect only the intended Ghost account and consider OOMOL's credential handling and usage charges.

## Reference(s):

- [Ghost Content API documentation](https://ghost.org/docs/content-api/)
- [oo CLI source](https://github.com/oomol-lab/oo-cli)
- [Ghost](https://ghost.org)

## Skill Output:

**Output Type(s):** [JSON, Text, Shell commands, Guidance]

**Output Format:** [JSON responses and shell command instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
