## Description: <br>
Integrate Blender MCP (Model Context Protocol) allowing OpenClaw to control Blender for 3D modeling, scene creation, and manipulation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mars720816](https://clawhub.ai/user/mars720816) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and 3D-content creators use this skill to connect OpenClaw to Blender through BlenderMCP so an agent can create, inspect, modify, and render Blender scenes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent broad control of Blender, including arbitrary Python execution. <br>
Mitigation: Review generated Blender Python before execution and prefer scoped Blender tools when possible. <br>
Risk: The local BlenderMCP socket could expose active Blender projects to unintended control. <br>
Mitigation: Keep the socket bound to localhost and work on copies of important Blender files. <br>
Risk: External Blender addons or MCP packages may affect project integrity. <br>
Mitigation: Install only trusted prompts, projects, Blender addons, and MCP packages. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/mars720816/openclaw-blender-mcp-skill) <br>
- [BlenderMCP project](https://github.com/ahujasid/blender-mcp) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code, configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands and Blender MCP tool requests] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can produce Blender Python instructions and scene-control requests; requires a local BlenderMCP socket connection.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
