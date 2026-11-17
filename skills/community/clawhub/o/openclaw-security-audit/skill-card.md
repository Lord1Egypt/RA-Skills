## Description:

Audit OpenClaw, Clawdbot, and Moltbot deployments for misconfigurations and attack vectors, including gateway exposure, control UI risk, skill safety, credential leakage, and hardening guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[misirov](https://clawhub.ai/user/misirov)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to perform read-only security reviews of OpenClaw, Clawdbot, or Moltbot environments and produce findings with impact explanations and fixes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The audit can expose sensitive host security details to the active agent session, including process, port, configuration, credential-path, service, cron, and log metadata.

Mitigation: Run it only from a trusted session, avoid root unless necessary, and limit sensitive host details in shared outputs.

Risk: Remediation guidance can include commands that affect services, credentials, firewall rules, or configuration when the user asks for fixes.

Mitigation: Keep execution read-only by default and review proposed remediation commands before approving them.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown terminal-style security audit report with summarized command evidence and remediation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only by default; remediation commands are proposed only after explicit user approval.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
