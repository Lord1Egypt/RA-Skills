## Description:

Scan your OpenClaw configuration for security risks and harden it with guided fixes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shanggqm](https://clawhub.ai/user/shanggqm)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill to audit OpenClaw configuration across DM policy, gateway exposure, group chat safety, tool permissions, sandboxing, file permissions, and model safety. After reporting findings, it can propose and apply user-selected hardening changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads OpenClaw configuration that may contain secrets.

Mitigation: Run a reviewed, pinned release and use it only in contexts where the agent is allowed to inspect OpenClaw configuration.

Risk: Optional hardening can edit configuration, change file permissions, and restart the Gateway.

Mitigation: Review the proposed plan before confirming execution and keep the generated backup available for rollback.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shanggqm/skills/guomeiqing-security-audit)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown security report with inline commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a scored audit, risk explanations, hardening plan options, and verification guidance.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
