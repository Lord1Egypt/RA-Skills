## Description:

Host security hardening and risk-tolerance configuration for OpenClaw deployments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[utromaya-code](https://clawhub.ai/user/utromaya-code)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to assess OpenClaw host security posture, plan firewall, SSH, update, backup, and exposure hardening, and perform approved remediation without breaking access.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Host security checks can expose sensitive local posture details such as hostnames, IP addresses, usernames, listening services, and credential locations.

Mitigation: Run read-only checks only with informed permission, redact sensitive details in summaries, and avoid saving raw outputs unless the user approves a specific storage location.

Risk: Firewall, SSH, package, service, scheduler, update policy, or memory-write actions can change host state or disrupt access.

Mitigation: Show exact commands before execution, require explicit approval for each state-changing step, preserve the confirmed access path, and use staged changes with rollback plans.

Risk: Scheduled audits or persisted memory entries can retain security-relevant system details.

Mitigation: Create cron jobs or memory entries only after explicit opt-in, use stable job names, and store redacted outputs in user-approved locations.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands, numbered choices, remediation plans, and posture reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires explicit approval before state-changing actions and avoids storing sensitive raw host details unless the user approves.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
