## Description:

Juniper JunOS device health check and triage procedure for assessing Routing Engine health, Packet Forwarding Engine state, chassis alarms, system resources, and environment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vahagn-madatyan](https://clawhub.ai/user/vahagn-madatyan)

### License/Terms of Use:

MIT-0

## Use Case:

Network operators, SREs, and support engineers use this skill to triage Juniper MX, SRX, EX, QFX, and PTX devices during incidents, audits, post-change checks, and capacity reviews. It guides collection and interpretation of JunOS health signals and produces a prioritized findings report with recommended actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release is labeled read-only while the runbook includes remediation guidance that may change devices, interrupt service, or remove data useful for rollback, incident response, or vendor support.

Mitigation: Treat diagnostic collection separately from remediation, require operator approval for device-changing commands, and run disruptive cleanup, rollback, reload, or power-cycle actions only under an approved change process.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/vahagn-madatyan/skills/juniper-device-health)
- [Juniper JunOS CLI Reference](references/cli-reference.md)
- [Juniper JunOS Threshold Tables](references/threshold-tables.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown runbook guidance with inline JunOS CLI commands and a findings report template]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only diagnostic posture is claimed, but reviewers should confirm remediation steps before execution.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
