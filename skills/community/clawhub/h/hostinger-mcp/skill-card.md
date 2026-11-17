## Description:

Operational guide for managing Hostinger infrastructure through the official Hostinger MCP server, including VPS, hosting, domains, DNS, Reach, and billing across one or several Hostinger accounts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[benkalsky](https://clawhub.ai/user/benkalsky)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use this skill to configure and use Hostinger MCP tools for account-scoped infrastructure operations, including read-only inventory and confirmed changes to VPS, hosting, domains, DNS, Reach, and billing resources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The connected MCP server can act with full Hostinger account authority through the account token.

Mitigation: Keep tokens in environment variables or a keychain, never print or commit them, and revoke and regenerate any token that may have been exposed.

Risk: Some tools can spend money, delete resources, wipe VPS data, or change billing settings.

Mitigation: Require explicit confirmation of the account, tool, target resource, parameters, impact, and cost before write or purchase actions; double-confirm destructive operations.

Risk: Installing or running the npm MCP package can execute package scripts and resolve dependencies at install time.

Mitigation: Prefer the documented pinned, digest-verified install path over the unverified npx convenience route when stronger supply-chain control is needed.

Risk: Multiple Hostinger accounts can expose similar resource IDs that are not interchangeable.

Mitigation: Use one connection per account, identify the account before every operation, and avoid carrying confirmations across accounts.

## Reference(s):

- [Installation - Hostinger MCP Server](references/installation.md)
- [Tools Catalog - Hostinger MCP](references/tools-catalog.md)
- [Workflows - VPS](references/workflows-vps.md)
- [Hostinger API MCP Server](https://github.com/hostinger/api-mcp-server)
- [Hostinger hPanel](https://hpanel.hostinger.com)
- [Hostinger API Reference](https://developers.hostinger.com/)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline shell commands and operational checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only operations are preferred by default; write, destructive, and billing actions require explicit user confirmation.]

## Skill Version(s):

1.2.1 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
