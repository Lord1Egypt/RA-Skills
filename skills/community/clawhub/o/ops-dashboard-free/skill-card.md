## Description: <br>
Ops Dashboard Free helps an agent inspect local operations status, including sessions, cron jobs, gateway health, basic security checks, and configuration state. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and small operations teams use this skill to run lightweight local checks for service health, active sessions, scheduled task status, configuration exposure, and basic security posture. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review reports a mismatch between read-only monitoring claims and write-capable metadata or modification-oriented instructions. <br>
Mitigation: Use the skill only for explicit local read-only dashboard checks, and do not grant write authority unless the publisher clarifies the conflicting instructions. <br>
Risk: Session, cron, configuration, and environment-check output can expose operational details or secrets. <br>
Mitigation: Keep outputs local, use authentication for dashboard requests, redact sensitive values before sharing, and avoid publishing raw scan or configuration results. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/ops-dashboard-free) <br>
- [Project homepage](https://skillhub.cn) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with command examples and operational status summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May summarize local session, cron, configuration, environment-check, and security-scan output that should be treated as sensitive.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
