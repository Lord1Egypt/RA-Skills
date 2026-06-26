## Description: <br>
Gstack OpenClaw is a prompt-only OpenClaw workflow pack that provides role-based engineering guidance for product planning, architecture, design review, security review, testing, deployment, monitoring, and retrospectives. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smseow001](https://clawhub.ai/user/smseow001) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to run structured OpenClaw workflows across product definition, technical design, code review, QA, release readiness, incident investigation, and project retrospectives. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated PR, deployment, rollback, browser-login, notification, or telemetry guidance could affect production systems if followed without review. <br>
Mitigation: Treat outputs as advisory, review generated commands and changes before use, require explicit authorization for high-impact actions, and prefer staging or test accounts first. <br>
Risk: Examples and workflows may involve OAuth tokens, API keys, repository access, or sensitive operational data. <br>
Mitigation: Use scoped credentials, redact secrets and sensitive data before sharing with external services, and avoid pasting production credentials into prompts. <br>
Risk: Server security evidence reports that the workflow pack under-scopes some high-impact production, repository, credential, browser-session, and notification guidance. <br>
Mitigation: Apply the server guidance: install through ClawHub, review each proposed code change or operational action, and keep generated guidance under human control. <br>


## Reference(s): <br>
- [Gstack OpenClaw on ClawHub](https://clawhub.ai/smseow001/gstack-openclaw-sms) <br>
- [Security Policy](artifact/SECURITY.md) <br>
- [Workflow Guide](artifact/docs/workflow.md) <br>
- [Garry Tan's gstack reference](https://github.com/garrytan/gstack) <br>
- [OpenClaw documentation](https://docs.openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with checklists, reports, code snippets, command examples, and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Prompt-only guidance; commands, code examples, credential use, deployments, rollbacks, notifications, and browser actions require user review and explicit authorization before execution.] <br>

## Skill Version(s): <br>
2.5.10 (source: server release metadata and artifact changelog, released 2026-04-10) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
