## Description:

Provides IT MSP tools for Azure/Microsoft 365 audits, NPU monitoring, firewall and SSH audits, update checks, and system health checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[phibuc87](https://clawhub.ai/user/phibuc87)

### License/Terms of Use:


## Use Case:

Developers and IT managed service provider operators use this skill to request agent assistance for Azure/Microsoft 365 status audits, infrastructure health checks, NPU monitoring, and administrative reset workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Supply-chain source or version mismatch during installation.

Mitigation: Verify the intended ClawHub package source, publisher handle, and version before installing.

Risk: Reset or reboot workflows may interrupt managed systems or services.

Mitigation: Treat reset and reboot actions as opt-in administrative operations and confirm maintenance impact before execution.

Risk: Operational audit guidance may be incomplete because the artifact contains only a sparse toolkit description.

Mitigation: Review proposed checks against the target environment and run standard security scanning before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/phibuc87/skills/msp-toolkit)
- [Publisher profile](https://clawhub.ai/user/phibuc87)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline commands and operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include administrative health-check or reset guidance that should be reviewed before execution.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
