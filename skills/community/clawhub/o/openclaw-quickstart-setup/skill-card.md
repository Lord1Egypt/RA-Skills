## Description: <br>
OpenClaw Quickstart Setup helps agents guide users through installing OpenClaw, hardening gateway settings, configuring model routing and channels, and enabling starter cron workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sepulchralvoid666](https://clawhub.ai/user/sepulchralvoid666) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to bootstrap an OpenClaw deployment, configure safer local gateway defaults, connect messaging channels, and add starter automations for daily briefs, email triage, and heartbeat checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent cron workflows can continue acting after initial setup if their scope and shutdown process are not defined. <br>
Mitigation: Enable cron workflows only after documenting allowed actions, session targets, monitoring expectations, and a clear stop or disable procedure. <br>
Risk: Messaging and email integrations can expose sensitive accounts or broad OAuth/API scopes. <br>
Mitigation: Use dedicated bot and email accounts where possible, restrict scopes to the minimum needed, protect tokens, and test integrations with non-sensitive data first. <br>
Risk: The skill asks users to install related skills such as wacli and maton. <br>
Mitigation: Verify those skills separately before installation and only allow reviewed skills in the OpenClaw configuration. <br>
Risk: Gateway exposure or weak authentication could make an OpenClaw instance reachable by unintended parties. <br>
Mitigation: Bind the gateway to 127.0.0.1, enable authentication, and use a private access layer such as Tailscale for remote access. <br>


## Reference(s): <br>
- [OpenClaw Quickstart Setup on ClawHub](https://clawhub.ai/sepulchralvoid666/openclaw-quickstart-setup) <br>
- [Publisher profile on ClawHub](https://clawhub.ai/user/sepulchralvoid666) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash and JSON code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces setup steps, configuration snippets, verification commands, troubleshooting guidance, and security cautions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
