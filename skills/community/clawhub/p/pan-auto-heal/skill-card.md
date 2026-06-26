## Description: <br>
自动监测并修复HTTP、端口、进程等服务异常，支持回滚到稳定状态，防止级联故障并发送告警。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[panjun2026](https://clawhub.ai/user/panjun2026) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to configure service health checks, restart or rollback commands, and alerting workflows for HTTP endpoints, ports, processes, containers, and command-based checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automatically run service restart, rollback, and other powerful configured commands. <br>
Mitigation: Review every configured command before use, restrict who can edit services.json, and avoid running as root or with sudo unless explicitly required. <br>
Risk: A health-check parsing issue could trigger repair or rollback commands unnecessarily. <br>
Mitigation: Fix and manually test health-check parsing before enabling cron or using the skill on production or critical services. <br>
Risk: Configuration examples may encourage storing operational secrets directly in command strings. <br>
Mitigation: Avoid plaintext credentials in services.json and use environment-specific secret management or least-privilege service accounts. <br>


## Reference(s): <br>
- [Auto-Heal configuration examples](references/examples.md) <br>
- [ClawHub skill page](https://clawhub.ai/panjun2026/pan-auto-heal) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JSON configuration examples and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include service check definitions, cron setup guidance, restart or rollback command patterns, and operational review notes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
