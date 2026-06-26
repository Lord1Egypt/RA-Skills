## Description: <br>
Teach an agent to install Provenote's first-party MCP server, connect it in a host, and run read-first outcome workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiaojiou176](https://clawhub.ai/user/xiaojiou176) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to connect a local Provenote MCP server in OpenHands or OpenClaw and run read-first note, research thread, and auditable run workflows before making a narrow write. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can lead an agent from read-only MCP inspection into write, download, chat, or settings-changing actions. <br>
Mitigation: Start with draft.list, research_thread.list, and auditable_run.list, then approve each write, download, chat, or settings mutation one at a time. <br>
Risk: A misconfigured or untrusted local Provenote repository could cause the host to launch the wrong MCP server. <br>
Mitigation: Install only from a Provenote repository you trust and use an absolute path to the intended local clone in the host configuration. <br>


## Reference(s): <br>
- [Install and Connect Provenote MCP](references/INSTALL.md) <br>
- [Provenote MCP Capabilities](references/CAPABILITIES.md) <br>
- [OpenHands / OpenClaw Demo Walkthrough](references/DEMO.md) <br>
- [OpenHands MCP Configuration](references/OPENHANDS_MCP_CONFIG.json) <br>
- [OpenClaw MCP Configuration](references/OPENCLAW_MCP_CONFIG.json) <br>
- [Provenote Troubleshooting](references/TROUBLESHOOTING.md) <br>
- [Provenote MCP Source Repository](https://github.com/xiaojiou176-open/provenote) <br>
- [ClawHub Skill Listing](https://clawhub.ai/xiaojiou176/provenote-mcp-outcome-workflows) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-first workflow guidance for MCP list calls, followed by one explicitly approved narrow mutation when appropriate.] <br>

## Skill Version(s): <br>
1.1.1 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
