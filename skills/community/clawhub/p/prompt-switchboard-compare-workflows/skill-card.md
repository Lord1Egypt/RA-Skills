## Description: <br>
Teach an agent to install Prompt Switchboard's local MCP sidecar, connect it in a host, and run a compare-first browser workflow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiaojiou176](https://clawhub.ai/user/xiaojiou176) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to install and connect Prompt Switchboard's local MCP sidecar, then compare one prompt across already-open AI chat tabs before broader automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup uses an external GitHub repository and npm dependencies for the local MCP sidecar. <br>
Mitigation: Review the referenced repository and dependency tree before installation, and run the sidecar from a trusted local clone. <br>
Risk: Compare workflows operate on already signed-in AI chat tabs and may send prompts to those providers or leave local compare history. <br>
Mitigation: Use only intended AI chat accounts and browser tabs, and avoid sensitive prompts unless the user accepts the provider and local-history exposure. <br>
Risk: Running compare before bridge and tab readiness are confirmed can fail or produce incomplete compare artifacts. <br>
Mitigation: Start with bridge_status and check_readiness, then stop and report missing login or tab preparation steps when fewer than two tabs are ready. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/xiaojiou176/prompt-switchboard-compare-workflows) <br>
- [Publisher profile](https://clawhub.ai/user/xiaojiou176) <br>
- [Install and Connect Prompt Switchboard MCP](references/INSTALL.md) <br>
- [Prompt Switchboard MCP Capabilities](references/CAPABILITIES.md) <br>
- [OpenHands / OpenClaw Demo Walkthrough](references/DEMO.md) <br>
- [Prompt Switchboard Troubleshooting](references/TROUBLESHOOTING.md) <br>
- [OpenHands MCP configuration](references/OPENHANDS_MCP_CONFIG.json) <br>
- [OpenClaw MCP configuration](references/OPENCLAW_MCP_CONFIG.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, MCP tool names, and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces compare-first workflow guidance and host setup instructions; it expects local browser tabs, a local MCP sidecar, and user-controlled provider sessions.] <br>

## Skill Version(s): <br>
1.1.1 (source: SKILL.md frontmatter and ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
