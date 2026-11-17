## Description:

SecurityTrails. Use this skill for ANY SecurityTrails request — searching and reading data. Whenever a task involves SecurityTrails, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and security practitioners use this skill to search SecurityTrails for associated domains, domain and DNS details, SSL certificate details, and subdomains through an OOMOL-connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup directs the agent to run a remote CLI installer whose contents have not been verified.

Mitigation: Review the setup first, use a verified CLI release, and require approval before running any downloaded installer.

Risk: Queries and connected credentials are handled through OOMOL.

Mitigation: Review the CLI's documented agent-skill synchronization and decide whether OOMOL should handle queries and connected credentials.

## Reference(s):

- [SecurityTrails API documentation](https://docs.securitytrails.com/docs/overview)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Text]

**Output Format:** [Structured SecurityTrails results as JSON with agent-readable text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only domain and DNS lookups; available data depends on SecurityTrails and the connected account.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
