## Description: <br>
OpenCode CLI guidance for submitting coding tasks, managing sessions, delegating work to coding agents, checking task status, and configuring OpenCode settings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tornado404](https://clawhub.ai/user/tornado404) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and coding-agent operators use this skill as a concise OpenCode and oho CLI handbook for creating sessions, sending coding tasks, monitoring work, handling timeouts, and configuring local OpenCode services. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide agents toward broad shell, file, permission, session, and server-control actions. <br>
Mitigation: Require explicit user approval before running shell commands, approving permissions, sharing or deleting sessions, attaching local files, changing provider credentials, or starting network-facing services. <br>
Risk: The artifact includes an example OpenCode server password and server startup commands. <br>
Mitigation: Replace sample credentials with a real secret-handling method and avoid exposing services unless the deployment is intentionally network-facing and access-controlled. <br>
Risk: Async sessions and MCP/server processes may continue running after task submission. <br>
Mitigation: Monitor started sessions and processes, check status before assuming completion, and stop services that are no longer needed. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/tornado404/opencode-client) <br>
- [OpenCode official docs](https://opencode.ai/docs/) <br>
- [OpenCode configuration schema](https://opencode.ai/config.json) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash and JSON code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes command examples, session-management procedures, timeout handling, server restart steps, and MCP configuration examples.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
