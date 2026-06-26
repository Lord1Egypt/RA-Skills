## Description: <br>
Integration patterns for using Mapbox MCP DevKit Server in AI coding assistants, covering setup, style management, token management, validation workflows, and documentation access. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mapbox](https://clawhub.ai/user/mapbox) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to configure Mapbox MCP DevKit access, manage Mapbox styles and tokens through an MCP-enabled assistant, and validate map assets before release. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Mapbox tokens can grant account access if exposed or over-scoped. <br>
Mitigation: Use hosted OAuth when possible, keep real tokens out of repositories and chat transcripts, and create least-privilege, domain-restricted tokens for each environment. <br>
Risk: Assistant-driven style, token, upload, update, or delete operations can affect production Mapbox assets. <br>
Mitigation: Require explicit confirmation before production changes and run style, expression, accessibility, and comparison checks before release. <br>


## Reference(s): <br>
- [Mapbox MCP DevKit Server](https://github.com/mapbox/mcp-devkit-server) <br>
- [Model Context Protocol](https://modelcontextprotocol.io) <br>
- [Mapbox Style Specification](https://docs.mapbox.com/style-spec/) <br>
- [Mapbox API Documentation](https://docs.mapbox.com/api/) <br>
- [Token Scopes Reference](https://docs.mapbox.com/api/accounts/tokens/) <br>
- [Setup & Installation](references/setup.md) <br>
- [Core Workflows](references/workflows.md) <br>
- [Design Patterns](references/design-patterns.md) <br>
- [Troubleshooting](references/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline JSON and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include tool-name recommendations and pre-production validation checklists.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
