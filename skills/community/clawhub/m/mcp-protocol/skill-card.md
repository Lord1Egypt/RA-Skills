## Description: <br>
配置和管理 MCP 服务器，使 AI 能够调用视觉理解、网络搜索等外部工具。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[godzff](https://clawhub.ai/user/godzff) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to set up mcporter and MCP server configuration so an AI agent can list servers and call tools such as MiniMax image understanding and web search. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: MCP servers can grant an agent access to external tools, local paths, or third-party APIs. <br>
Mitigation: Review each enabled MCP server before installation, use least-privilege filesystem paths, and scope API or GitHub tokens narrowly. <br>
Risk: The setup guidance includes installing uv through a remote shell command. <br>
Mitigation: Prefer installing uv through a package manager or inspect the installer before running it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/godzff/mcp-protocol) <br>
- [Astral uv installer referenced by the skill](https://astral.sh/uv/install.sh) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with bash and JSON code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes example MCP server configuration and validation commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
