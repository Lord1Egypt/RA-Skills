## Description: <br>
Operational guide for managing Hostinger infrastructure, including VPS, hosting, domains, DNS, email marketing, and billing, through the official Hostinger MCP server across one or more Hostinger accounts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[benkalsky](https://clawhub.ai/user/benkalsky) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to install and operate Hostinger's MCP server, select the right Hostinger tool category, and manage infrastructure tasks with explicit confirmation for account, cost, destructive, and write actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Connected Hostinger MCP tools can make purchases, change billing settings, modify DNS, rebuild VPS instances, delete resources, and otherwise exercise broad account authority. <br>
Mitigation: Use separate tokens per account, load only the needed Hostinger category binary, and require explicit account, target, impact, and cost confirmation before any write, purchase, billing change, DNS change, deletion, or VPS rebuild. <br>
Risk: Hostinger API tokens provide full account access through the connected MCP server. <br>
Mitigation: Treat tokens as sensitive credentials, avoid printing or committing them, and keep each account on its own MCP connection and token. <br>


## Reference(s): <br>
- [Hostinger MCP Server](https://github.com/hostinger/api-mcp-server) <br>
- [Hostinger hPanel](https://hpanel.hostinger.com) <br>
- [Installation - Hostinger MCP Server](references/installation.md) <br>
- [Tools Catalog - Hostinger MCP](references/tools-catalog.md) <br>
- [Workflows - VPS](references/workflows-vps.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, API calls, Markdown] <br>
**Output Format:** [Markdown guidance with shell commands, MCP tool names, and confirmation prompts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces operational instructions and confirmation patterns; it does not itself execute Hostinger actions without connected MCP tools.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
