## Description: <br>
Host security hardening and risk-tolerance configuration for OpenClaw deployments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rmbell09-lang](https://clawhub.ai/user/rmbell09-lang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and OpenClaw users use this skill to assess host exposure, choose a risk posture, plan security hardening, and guide approved firewall, SSH, update, audit, and scheduling actions without disrupting access. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Security-hardening guidance can affect host access, firewall policy, SSH/RDP configuration, services, update behavior, packages, scheduled tasks, and local memory files. <br>
Mitigation: Ask for explicit approval before read-only checks and each state-changing step, show exact commands, explain impact and rollback, preserve the current access path, and stop on unexpected output. <br>
Risk: OpenClaw hardening may be confused with host-level operating system hardening. <br>
Mitigation: State that OpenClaw security fixes tighten OpenClaw defaults and file permissions only, and treat firewall, SSH, updates, services, and OS settings as separate user-approved actions. <br>
Risk: Audit logs, memory writes, or scheduled audit output could expose sensitive host details or credentials. <br>
Mitigation: Redact secrets and sensitive host identifiers, avoid logging tokens or credential contents, store outputs only in user-approved locations, and write memory only after explicit opt-in. <br>


## Reference(s): <br>
- [Lucky Healthcheck on ClawHub](https://clawhub.ai/rmbell09-lang/lucky-healthcheck) <br>
- [Publisher profile: rmbell09-lang](https://clawhub.ai/user/rmbell09-lang) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with numbered choices and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires explicit user approval before checks, state-changing commands, scheduling, or memory writes; final output may include remediation plans, rollback notes, and posture reports.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
