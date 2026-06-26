## Description: <br>
OpenCode Remote uses the OpenCode HTTP API to manage remote sessions, send prompts, monitor progress, and select agents for new sessions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Entropy-xcy](https://clawhub.ai/user/Entropy-xcy) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to operate remote OpenCode servers by listing sessions, sending prompts, monitoring work progress, creating sessions, and checking task state through the OpenCode API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Remote OpenCode endpoints and local SOCKS proxies can expose prompts, session data, or command traffic to untrusted infrastructure. <br>
Mitigation: Use only trusted endpoints and network paths, prefer HTTPS or a trusted private network, and verify the endpoint before each action. <br>
Risk: Shell, delete, abort, and fork operations can materially alter remote sessions or systems. <br>
Mitigation: Treat these operations as privileged actions and require explicit user confirmation before invoking them. <br>
Risk: Automatic monitoring can continue polling remote sessions after it is no longer needed. <br>
Mitigation: Disable monitoring once the task is complete or when continued session observation is no longer required. <br>
Risk: Prompts sent to remote sessions may contain secrets or sensitive project details. <br>
Mitigation: Avoid sending secrets and repeat prompt content back to the user for confirmation before or immediately after transmission. <br>


## Reference(s): <br>
- [OpenCode API Reference](references/api_reference.md) <br>
- [ClawHub release page](https://clawhub.ai/Entropy-xcy/opencode-remote) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline API examples, shell commands, JSON responses, and concise status summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include remote session identifiers, endpoint-specific command examples, monitoring summaries, and confirmation text for prompts sent to OpenCode sessions.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
