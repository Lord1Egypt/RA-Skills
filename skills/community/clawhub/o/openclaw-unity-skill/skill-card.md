## Description: <br>
Control Unity Editor via OpenClaw Unity Plugin for Unity game development tasks including scene management, GameObject and component manipulation, debugging, input simulation, and Play mode control. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TomLeeLive](https://clawhub.ai/user/TomLeeLive) <br>

### License/Terms of Use: <br>
Apache 2.0 <br>


## Use Case: <br>
Developers and engineers use this skill to inspect and control Unity Editor projects through OpenClaw workflows, including scene editing, asset and package operations, test running, screenshots, and Play mode automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can modify Unity projects through editor, scene, object, component, asset, and package operations. <br>
Mitigation: Use version control or backups before running workflows, test in a separate project first, and review project-changing actions before execution. <br>
Risk: The bridge exposes high-impact actions such as script execution, package installation or removal, asset deletion, save operations, input automation, and batch execution. <br>
Mitigation: Keep disableModelInvocation enabled and require explicit human approval before using these actions. <br>
Risk: Gateway or bridge access can allow remote control of a connected Unity Editor session. <br>
Mitigation: Restrict gateway and MCP bridge access to trusted local use and install only when OpenClaw should control the Unity project. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/TomLeeLive/openclaw-unity-skill) <br>
- [Unity tool reference](references/tools.md) <br>
- [OpenClaw Unity Plugin](https://github.com/TomLeeLive/openclaw-unity-plugin) <br>
- [OpenClaw documentation](https://docs.openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline commands, tool names, code snippets, and configuration instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide agents to issue Unity Editor control commands through OpenClaw or an MCP bridge.] <br>

## Skill Version(s): <br>
1.6.1 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
