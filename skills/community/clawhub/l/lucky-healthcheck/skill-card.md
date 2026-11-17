## Description:

Host security hardening and risk-tolerance configuration for OpenClaw deployments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rmbell09-lang](https://clawhub.ai/user/rmbell09-lang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to assess and harden hosts running OpenClaw, including security audits, firewall and SSH review, update posture, risk-tolerance alignment, and optional periodic checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Host hardening commands can disrupt remote access or services if applied without review.

Mitigation: Require explicit approval for each state-changing command, confirm the access path first, and include rollback guidance before execution.

Risk: Security audits may inspect sensitive host state or credential locations.

Mitigation: Start with user-approved read-only checks, redact secrets in reports and logs, and avoid accessing credential contents unless explicitly approved.

Risk: Scheduling recurring audits or writing memory can create persistent host changes.

Mitigation: Create cron jobs or memory entries only after direct user opt-in and show the exact command or entry before applying it.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, numbered choices, remediation plans, and final posture reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires explicit user approval before state-changing host changes; read-only checks are requested before execution.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
