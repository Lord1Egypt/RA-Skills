## Description: <br>
Lu Nas Monitor helps agents monitor NAS Docker container status, system resources, service health, logs, and optional alert notifications. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jesson1222-ship-it](https://clawhub.ai/user/jesson1222-ship-it) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and NAS administrators use this skill to ask an agent for NAS service checks, including Docker container state, CPU and memory use, disk space, service health, logs, and alert examples. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Routine monitoring prompts could lead to service-impacting commands such as restarting Docker Compose services. <br>
Mitigation: Keep monitoring read-only by default and require explicit user approval before any restart or other service-changing command. <br>
Risk: Logs, hostnames, internal service details, or Telegram alert configuration can expose sensitive NAS information. <br>
Mitigation: Redact secrets and internal details before sharing outputs, and only use Telegram notifications when that third-party path is acceptable. <br>


## Reference(s): <br>
- [Lu Nas Monitor ClawHub page](https://clawhub.ai/jesson1222-ship-it/lu-nas-monitor) <br>
- [Skill instructions](artifact/SKILL.md) <br>
- [Skill metadata](artifact/_meta.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with bash command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Docker, system monitoring, log inspection, restart, and Telegram alert command examples.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, artifact/_meta.json, artifact/SKILL.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
