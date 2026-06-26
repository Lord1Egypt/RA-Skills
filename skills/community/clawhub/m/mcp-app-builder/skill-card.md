## Description: <br>
Builds new MCP Apps with React UI output using @modelcontextprotocol/ext-apps and the MCP SDK. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hollaugo](https://clawhub.ai/user/hollaugo) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to scaffold or implement MCP App servers that return React UI resources, including tool schemas, server wiring, Vite single-file UI bundles, and host-theme-aware React components. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated MCP apps may later be connected to private APIs, business data, or public tunnels without sufficient access control. <br>
Mitigation: Add authentication and origin restrictions before exposing generated apps or using sensitive data. <br>
Risk: Template dependencies can drift or introduce supply-chain risk if installed without review. <br>
Mitigation: Pin npm dependencies, commit a lockfile, and review dependency updates before deployment. <br>
Risk: Tool-specific data sources added after scaffolding can change the security posture of the generated app. <br>
Mitigation: Review each added data source and its handling of sensitive inputs before deployment. <br>


## Reference(s): <br>
- [MCP App Specification](artifact/references/mcp-app-spec.md) <br>
- [Mcp App Builder on ClawHub](https://clawhub.ai/hollaugo/mcp-app-builder) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with code snippets, shell commands, and scaffolded file contents.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should preserve the exact MCP App dependency versions and server/UI patterns specified by the bundled reference.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
