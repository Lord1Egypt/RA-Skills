## Description: <br>
Control FreeCAD via MCP to create and modify 3D models, automate CAD tasks, solve constraints, and integrate part libraries programmatically. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mars720816](https://clawhub.ai/user/mars720816) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and CAD automation users use this skill to connect MCP-enabled agents to FreeCAD for creating, editing, inspecting, and generating 3D models from prompts or structured commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Connected agents can execute unscoped Python code and broadly control FreeCAD documents. <br>
Mitigation: Install only for trusted agents and packages, use copies of important CAD files, and avoid exposing execute_code to untrusted or autonomous agents. <br>
Risk: The RPC bridge can create, edit, delete, and inspect CAD documents through the local FreeCAD session. <br>
Mitigation: Keep the RPC server bound to localhost, stop it when not in use, and review generated CAD changes before relying on them. <br>


## Reference(s): <br>
- [FreeCAD MCP ClawHub page](https://clawhub.ai/mars720816/openclaw-freecad-mcp) <br>
- [Skill instructions](artifact/SKILL.md) <br>
- [Artifact README](artifact/README.md) <br>
- [FreeCAD parts library](https://github.com/FreeCAD/FreeCAD-library) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and tool guidance with JSON configuration and command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return text status, CAD object data, and image previews from FreeCAD views when available.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
