## Description:

Linux Security Scanner audits Linux hosts for SSH settings, listening ports, firewall rules, failed login attempts, sudoers permissions, world-writable files, and SUID binaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[laolaoqi](https://clawhub.ai/user/laolaoqi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, system administrators, and security engineers use this skill to run local Linux security posture checks and collect a formatted audit report for hardening review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Crafted SSH configuration values may be turned into shell commands by the audit script, which is risky during privileged execution.

Mitigation: Review and fix the shell script before installation; avoid running it as sudo/root on systems where SSH configuration content might be attacker-controlled, and replace the dynamic bash -c SSH summary with fixed printf-style handling.

Risk: Some checks read privileged system state such as failed-login logs and process details.

Mitigation: Run the audit only on systems you are authorized to inspect, and handle generated reports as security-sensitive operational data.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/laolaoqi/skills/linux-security-scanner)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with bash commands and a shell-script audit report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The audit script prints a colorized stdout report and stores a structured markdown report in the REPORT variable during execution.]

## Skill Version(s):

1.0.0 (source: server release evidence, released 2026-05-11)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
