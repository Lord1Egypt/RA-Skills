## Description: <br>
Interact with Meegle project management system via MCP protocol <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pkycy](https://clawhub.ai/user/pkycy) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, operators, and project teams use this skill to connect an agent to Meegle so it can list and manage projects, tasks, workflows, members, and reports through the MCP server. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Authenticated Meegle operations can make real workspace changes, including creating projects, moving tasks, adding members, or changing permissions. <br>
Mitigation: Install only for trusted workspaces, review prompts before write actions, and use least-privilege or service-account credentials where possible. <br>
Risk: The setup script can persist Meegle credentials in shell startup files. <br>
Mitigation: Prefer secure environment management, avoid syncing shell profiles that contain secrets, and rotate keys if they are exposed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/pkycy/meegle-mcp-skill) <br>
- [Meegle official website](https://www.meegle.com/) <br>
- [Meegle overview](https://www.larksuite.com/hc/en-US/articles/040270863407-meegle-overview) <br>
- [Model Context Protocol specification](https://modelcontextprotocol.io/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and agent text with inline shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May trigger authenticated MCP requests that read or modify Meegle workspace data, depending on the user's credentials and prompt.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
