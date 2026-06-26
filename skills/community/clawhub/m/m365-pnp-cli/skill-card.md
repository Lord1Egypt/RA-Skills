## Description: <br>
CLI for Microsoft 365 - Manage Microsoft 365 tenant, SharePoint Online, Teams, OneDrive, and more. Official PnP (Patterns and Practices) CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thomyg](https://clawhub.ai/user/thomyg) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, administrators, and agents use this skill to operate the Microsoft 365 CLI for tenant, SharePoint Online, Teams, OneDrive, Outlook, Planner, and Entra ID management tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access or change Microsoft 365 tenant data when authenticated with a privileged account. <br>
Mitigation: Use least-privileged accounts and require explicit confirmation before tenant-wide enumeration, sensitive reads, write operations, or administrative commands. <br>
Risk: Credential handling choices can increase exposure during Microsoft 365 authentication. <br>
Mitigation: Prefer device-code or certificate-based authentication over username/password or client secrets. <br>
Risk: The skill depends on the external @pnp/cli-microsoft365 npm package and the m365 binary. <br>
Mitigation: Verify the npm package source and version before installation or execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thomyg/m365-pnp-cli) <br>
- [CLI for Microsoft 365 documentation](https://pnp.github.io/cli-microsoft365) <br>
- [CLI for Microsoft 365 npm package](https://www.npmjs.com/package/@pnp/cli-microsoft365) <br>
- [CLI for Microsoft 365 repository](https://github.com/pnp/cli-microsoft365) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce or request JSON, text, and JMESPath-filtered CLI output from m365 commands.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
