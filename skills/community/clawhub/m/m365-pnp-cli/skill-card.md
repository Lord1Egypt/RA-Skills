## Description:

CLI for Microsoft 365 - Manage Microsoft 365 tenant, SharePoint Online, Teams, OneDrive, and more. Official PnP (Patterns and Practices) CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thomyg](https://clawhub.ai/user/thomyg)

### License/Terms of Use:


## Use Case:

Developers and administrators use this skill to operate the CLI for Microsoft 365 for tenant, SharePoint Online, Teams, OneDrive, Outlook, Planner, and Entra ID management tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can help run Microsoft 365 CLI commands with broad tenant visibility or modification capability.

Mitigation: Use least-privilege Microsoft 365 accounts or app permissions and confirm before running commands that create, modify, delete, or broadly enumerate tenant data.

Risk: Installing or running the CLI from an unreviewed package version can introduce supply-chain risk.

Mitigation: Install only from a trusted npm source and consider pinning a reviewed @pnp/cli-microsoft365 version.

Risk: Username/password authentication is less appropriate for agent-driven or automated use.

Mitigation: Avoid username/password authentication; prefer device code for interactive use or certificate-based authentication for production automation.

## Reference(s):

- [CLI for Microsoft 365 documentation](https://pnp.github.io/cli-microsoft365)
- [CLI for Microsoft 365 npm package](https://www.npmjs.com/package/@pnp/cli-microsoft365)
- [CLI for Microsoft 365 repository](https://github.com/pnp/cli-microsoft365)
- [ClawHub skill page](https://clawhub.ai/thomyg/skills/m365-pnp-cli)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and CLI output expectations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [CLI commands may return JSON or text; Node.js >= 20, the m365 binary, and Microsoft 365 authentication are required.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
