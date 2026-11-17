## Description:

Diagnose and recover OpenClaw node connectivity over SSH tunnel.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xyezir](https://clawhub.ai/user/xyezir)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to diagnose and recover OpenClaw node connectivity failures involving SSH tunnels, pairing-required errors, port conflicts, remote endpoint mismatches, credential checks, and unstable node status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: SSH targets, endpoints, node identifiers, and gateway credentials may expose sensitive operational details if copied into external reports.

Mitigation: Use placeholders for all network, identity, and credential fields before sharing reports outside the trusted operational context.

Risk: Incorrect SSH tunnel or endpoint changes can leave a node unreachable or unstable.

Mitigation: Validate the local forward, confirm the tunnel-local endpoint and SSH target, then re-run probe and status checks before recording the outcome.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xyezir/skills/oc-ssh-tunnel-node-recovery)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with root cause, ordered fixes, verification evidence, residual risk, and next action.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Network, identity, and credential values should be replaced with placeholders in external reports.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
