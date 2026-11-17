## Description:

Verifies and configures required MCP servers for the Product Guide Writer workflow, especially Atlassian and GitHub integrations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tsvetelin-kulinski](https://clawhub.ai/user/tsvetelin-kulinski)

### License/Terms of Use:


## Use Case:

Developers and product documentation authors use this skill to check whether required MCP servers are available and authenticated for Product Guide Writer workflows. It also provides setup and troubleshooting guidance for Atlassian, Confluence, GitHub, and optional supporting MCP integrations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The GitHub MCP setup may execute a mutable package version through npx -y.

Mitigation: Pin and review the MCP server package version before installation or execution.

Risk: The setup guidance may lead users to grant broad or long-lived GitHub token access.

Mitigation: Use fine-grained or read-only tokens scoped only to the repositories and organization access required, and rotate any token that may have been exposed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tsvetelin-kulinski/skills/github-mpc)
- [README.md](artifact/README.md)
- [SKILL.md](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with inline JSON and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces setup checks, validation checklists, and troubleshooting steps for MCP server configuration.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
