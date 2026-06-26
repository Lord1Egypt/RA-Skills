## Description: <br>
Minimal MCP server example for invoking add and hello_world tools in OpenClaw. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Crystaria](https://clawhub.ai/user/Crystaria) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and learners use this skill as a small MCP server example for testing OpenClaw MCP integration, adding two numbers, returning greetings, and adapting the template for simple tool-server development. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs npm dependencies and runs a local Node.js MCP server. <br>
Mitigation: Review package.json and package-lock.json before installation in stricter environments, then run it in a local demo or development context. <br>
Risk: The exposed tools are simple demo utilities and are suitable only for low-risk examples. <br>
Mitigation: Use the add and hello_world tools for testing, teaching, or template development rather than high-stakes workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Crystaria/mcp-hello-world) <br>
- [MCP official documentation](https://modelcontextprotocol.io) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [README.md](artifact/README.md) <br>
- [package.json](artifact/package.json) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration] <br>
**Output Format:** [MCP text responses with Markdown documentation and bash command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs as a local Node.js MCP server over stdio and exposes add and hello_world tools.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata and SKILL.md changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
