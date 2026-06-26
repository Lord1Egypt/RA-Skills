## Description: <br>
Pixcake Skills helps agents operate the PixCake desktop client for project management, preset retouching, and export tasks through PixCake MCP tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jasperdon](https://clawhub.ai/user/jasperdon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External PixCake users and developers use this skill to connect an agent to a local PixCake desktop client, manage projects, import images, apply preset retouching, submit exports, and check export status. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Setup may install mcporter globally with npm and persistently update the OpenClaw MCP configuration. <br>
Mitigation: Run the setup script in check-only mode first, review the discovered PixCake and pixcake-mcp paths, and proceed only if persistent MCP configuration changes are acceptable. <br>
Risk: An incorrect PixCake or pixcake-mcp path could produce a broken or unintended MCP configuration. <br>
Mitigation: Use explicit paths when auto-discovery is uncertain and verify the pixcake server with mcporter before calling PixCake tools. <br>
Risk: Export submission is asynchronous and can be mistaken for completed export output. <br>
Mitigation: Treat batch_export_images as task submission and use get_task_status before saying an export has completed. <br>
Risk: Requests outside the exposed PixCake tool surface could lead to unsupported probing or misleading responses. <br>
Mitigation: Stay within project management, preset retouching, and export workflows, and state that unsupported features are not exposed by this skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jasperdon/pixcake) <br>
- [Capability Map](references/capabilities.md) <br>
- [Compatibility](references/compatibility.md) <br>
- [Projects](references/projects.md) <br>
- [Retouch](references/retouch.md) <br>
- [Export](references/export.md) <br>
- [MCPorter setup](references/mcp-setup.md) <br>
- [Response Policy](references/response-policy.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and MCP tool-call examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May invoke MCP tools that create projects, import images, apply presets, submit exports, and query export status.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
