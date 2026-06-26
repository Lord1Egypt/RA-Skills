## Description: <br>
High-performance coding agent and browser automation orchestrator using the Kilo CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sabyaghosh](https://clawhub.ai/user/sabyaghosh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering agents use this skill to delegate large coding tasks, multi-file refactors, browser automation workflows, and Kilo session management to the Kilo CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Hands-free Kilo execution can perform broad coding or browser actions without interactive review. <br>
Mitigation: Keep runs constrained to trusted workspaces and domains, and avoid auto-approval for destructive changes, account actions, secrets, form submissions, or sensitive browsing. <br>
Risk: MCP server setup can extend the agent with local package-backed browser and filesystem capabilities. <br>
Mitigation: Review MCP packages and configuration before enabling them, and enable only the servers required for the intended task. <br>
Risk: Continuing or forking sessions can carry context across users, credentials, or security boundaries. <br>
Mitigation: Start fresh sessions when switching users, credentials, or security contexts. <br>


## Reference(s): <br>
- [Kilo CLI Setup and Configuration](references/setup-guide.md) <br>
- [Kilo CLI Workflow for OpenClaw](references/workflow.md) <br>
- [ClawHub release page](https://clawhub.ai/sabyaghosh/openclaw-kilo-agent) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May initiate Kilo CLI sessions and MCP-backed browser automation when executed by an agent.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
