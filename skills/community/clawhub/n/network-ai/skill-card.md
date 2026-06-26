## Description: <br>
Network AI is a local Python orchestration skill for multi-agent workflows using a shared blackboard file, permission gating, token budget scripts, and persistent project context. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jovancoding](https://clawhub.ai/user/jovancoding) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to coordinate multi-agent work locally, track shared task state, manage budget checks, and request advisory permission grants before sensitive operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores shared blackboard state, project context, audit logs, and advisory grant records in local workspace files. <br>
Mitigation: Keep the data directory private, restrict local file permissions, and review project-context.json before injecting it into prompts. <br>
Risk: Permission grant tokens are advisory scoring outputs and do not authenticate the caller's identity. <br>
Mitigation: Require separate identity verification or human approval before honoring grants for sensitive resources such as payments, databases, email, or file export. <br>
Risk: Free-text permission justifications and project context may contain sensitive data if agents or users enter it. <br>
Mitigation: Do not place PII, credentials, or secrets in justification fields or project context, and rotate or delete local audit logs as needed. <br>
Risk: The broader npm package can expose optional shell execution or a local MCP SSE server when an operator explicitly enables those features. <br>
Mitigation: Keep shell auto-approval disabled outside isolated test environments, require a bearer token for MCP access, and bind local services only to trusted interfaces. <br>


## Reference(s): <br>
- [Network AI homepage](https://network-ai.org) <br>
- [ClawHub skill page](https://clawhub.ai/jovancoding/network-ai) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, markdown, JSON] <br>
**Output Format:** [Markdown instructions with bash examples and local JSON or markdown file outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs and state remain local unless the host platform or operator connects external services.] <br>

## Skill Version(s): <br>
5.12.7 (source: target metadata and evidence.release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
