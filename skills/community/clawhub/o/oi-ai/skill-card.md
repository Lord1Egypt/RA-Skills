## Description: <br>
Load Oi Contexts and Workflows from MCP when the user says oi, names a Context or Workflow, or wants sticky Oi context. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[carhaix](https://clawhub.ai/user/carhaix) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use Oi to discover, load, install, tune, publish, and run Oi Contexts and Workflows through the hosted MCP server, with approval gates for account-affecting actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill connects OpenClaw to the hosted Oi MCP server and may store OAuth tokens or an organization API key. <br>
Mitigation: Prefer OAuth for interactive setup, keep bearer tokens in secrets or environment variables, and rotate organization API keys if access changes or a token is exposed. <br>
Risk: Approved Oi actions may affect Contexts, Workflows, organization settings, billing, API keys, durable feedback, or connected provider data. <br>
Mitigation: Require explicit user approval before install, publish, write, billing, organization, credential, durable-feedback, or connected-provider actions. <br>
Risk: Running Contexts or connection tools can involve private user, organization, or provider data. <br>
Mitigation: Ask for approval before using private data or external connection tools, and do not save secrets or one-off task details as durable feedback. <br>


## Reference(s): <br>
- [ClawHub Oi listing](https://clawhub.ai/carhaix/oi-ai) <br>
- [OpenClaw Oi repository](https://github.com/openclaw/oi-openclaw) <br>
- [Oi MCP authentication guide](https://www.oioioi.ai/resources/authentication) <br>
- [OpenClaw MCP CLI](https://docs.openclaw.ai/cli/mcp) <br>
- [Oi MCP Authentication for OpenClaw](references/authentication.md) <br>
- [Oi MCP Tools](references/mcp-tools.md) <br>
- [Oi Product Surfaces](references/product-surfaces.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and MCP tool-selection guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May trigger Oi MCP calls after user approval; usage reporting is limited to runtime and token metadata the client actually knows.] <br>

## Skill Version(s): <br>
0.1.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
