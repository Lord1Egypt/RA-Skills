## Description: <br>
Play Command & Conquer Red Alert RTS by building bases, training armies, and defeating AI opponents through 48 MCP tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yxc20089](https://clawhub.ai/user/yxc20089) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External developers and agent users use this skill to connect an agent to OpenRA-RL, configure the local MCP server, observe Red Alert game state, and issue gameplay commands through the documented tool interface. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs third-party Python code and starts a Docker-backed local game server. <br>
Mitigation: Review the package or image provenance before use, run it in an isolated development environment, and stop the server or container when finished. <br>
Risk: The game server depends on Docker and local port availability, so it may fail or conflict in constrained environments. <br>
Mitigation: Confirm Docker is installed and available, then verify server status before connecting the MCP configuration. <br>


## Reference(s): <br>
- [OpenRA-RL Homepage](https://github.com/yxc20089/OpenRA-RL) <br>
- [OpenRA-RL PyPI Package](https://pypi.org/project/openra-rl/) <br>
- [OpenRA-Bench Leaderboard](https://huggingface.co/spaces/yxc20089/OpenRA-Bench) <br>
- [ClawHub Skill Page](https://clawhub.ai/yxc20089/openra-rl) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with tables, shell command snippets, and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Provides game strategy and MCP tool-use guidance; the skill requires Docker for the local game server.] <br>

## Skill Version(s): <br>
1.1.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
