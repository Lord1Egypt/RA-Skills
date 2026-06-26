## Description: <br>
Monitor critical processes and auto-restart on failure, with CPU and memory checks, webhook, callback, or file alerts, dead man's switch heartbeat output, and an optional HTTP status dashboard. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TheShadowRose](https://clawhub.ai/user/TheShadowRose) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to add a local watchdog for critical services, including health checks, controlled restarts, status reporting, heartbeat files, and alert escalation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can restart local services using configured commands. <br>
Mitigation: Use commandAllowlist, avoid allowAnyCommand unless the configuration is fully trusted, and run the watchdog under a least-privileged service account. <br>
Risk: The optional dashboard can expose local process status. <br>
Mitigation: Keep dashboard access local or protect it behind trusted network controls. <br>
Risk: Webhook alerts send operational data to an external endpoint when configured. <br>
Mitigation: Send webhooks only to trusted endpoints and review alert contents before enabling external delivery. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/TheShadowRose/process-guard) <br>
- [Artifact README](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JavaScript, JSON, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs guidance for configuring local process monitoring, restart policy, alerting, heartbeat files, and the optional dashboard.] <br>

## Skill Version(s): <br>
2.1.4 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
