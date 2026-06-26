## Description: <br>
Godot MCP (Model Context Protocol) integration enabling AI assistants to directly interact with Godot Editor for scene creation, node manipulation, script editing, resource management, project control, and AI client setup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thb32133451](https://clawhub.ai/user/thb32133451) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and game teams use this skill to connect AI clients to a local Godot MCP server so an assistant can help inspect, create, modify, and save Godot scenes, nodes, scripts, resources, and project settings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: AI clients connected through the local MCP server can broadly modify Godot project files, scenes, scripts, and resources, including destructive file operations. <br>
Mitigation: Use project-level configuration, keep the project in version control, and require explicit approval before file deletion, script overwrites, scene saves, or bulk edits. <br>
Risk: The server evidence reports insufficient documented safety controls for broad project-editing and deletion power. <br>
Mitigation: Review and pin the external plugin source, disable auto-start when not needed, and scan changes before deployment. <br>


## Reference(s): <br>
- [Godot MCP Integration ClawHub page](https://clawhub.ai/thb32133451/godot-mcp) <br>
- [Godot MCP API Quick Reference](references/api-reference.md) <br>
- [Godot MCP Usage Examples](references/examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON tool-call examples, and code snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides an agent to configure MCP clients and operate Godot project tools through a local MCP server.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
